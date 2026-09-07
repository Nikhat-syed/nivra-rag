"""
Stage 9 — Grounded RAG Generation & Multilingual Plain-Language Translation
Uses Groq API (Llama-3.3-70b / Llama-3.1-8b) to synthesize strictly grounded answers with citations.
Generates:
  1. Official Wording with exact citations
  2. Simplified Plain-Language Rewrite (low digital literacy)
Translates the Plain-Language rewrite into Telugu and Hindi via deep-translator.
Includes offline context synthesizer fallback.
"""

import os
import sys
import logging
from typing import List, Dict, Any, Tuple
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 stdout for Windows CLI
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    except Exception:
        pass

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class SchemeAnswerGenerator:
    def __init__(self, groq_api_key: str = None, openai_api_key: str = None, gemini_api_key: str = None):
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY", "").strip()
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY", "").strip()
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY", "").strip()

        self.groq_client = None
        self.openai_client = None

        if self.groq_api_key and not self.groq_api_key.startswith("your_"):
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=self.groq_api_key)
                logger.info("Initialized Groq LLM client.")
            except Exception as e:
                logger.warning(f"Could not initialize Groq SDK: {e}")

        if self.openai_api_key and not self.openai_api_key.startswith("your_"):
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=self.openai_api_key, max_retries=0, timeout=4.0)
                logger.info("Initialized OpenAI LLM client.")
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI SDK: {e}")

    def format_context_prompt(self, chunks: List[Dict[str, Any]]) -> str:
        """Formats retrieved chunks into structured context blocks for prompt injection."""
        context_blocks = []
        for idx, c in enumerate(chunks, start=1):
            block = (
                f"[Doc {idx}]\n"
                f"Scheme Name: {c.get('scheme_name')}\n"
                f"Section: {c.get('section_title')}\n"
                f"Category: {c.get('category')} | Target: {c.get('target_group')} | State: {c.get('state_or_central')}\n"
                f"Content:\n{c.get('text')}\n"
            )
            context_blocks.append(block)
        return "\n----------------------------------------\n".join(context_blocks)

    def generate_answers(
        self, query: str, chunks: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Generates both Official Wording (with citations) and Simplified Plain Language answers.
        """
        if not chunks:
            no_info_msg = "I do not have enough official information in the retrieved scheme documents to answer this question."
            return {
                "official_answer": no_info_msg,
                "plain_answer": "No scheme information was found for your query. Please try adjusting your search terms."
            }

        context_str = self.format_context_prompt(chunks)

        system_prompt = (
            "You are Nivra, an AI assistant empowering women entrepreneurs.\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. Answer EVERY single user question directly, accurately, and comprehensively.\n"
            "2. When retrieved scheme context is relevant to the question, strictly ground the scheme details in the context and include citations: [Source: Scheme Name - Section Title].\n"
            "3. If the question is a general query, provide a complete helpful answer first, then highlight relevant government schemes or support resources for women entrepreneurs.\n"
        )

        user_prompt = (
            f"USER QUESTION: {query}\n\n"
            f"RETRIEVED SCHEME CONTEXT:\n{context_str}\n\n"
            "Generate your answer in two sections:\n"
            "OFFICIAL_ANSWER:\n<Detailed comprehensive answer with scheme citations if applicable>\n\n"
            "PLAIN_LANGUAGE_ANSWER:\n<Simplified 3-bullet point summary>\n"
        )

        # Try OpenAI API first if key is present
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=900
                )
                raw_text = response.choices[0].message.content
                if "PLAIN_LANGUAGE_ANSWER:" in raw_text:
                    parts = raw_text.split("PLAIN_LANGUAGE_ANSWER:")
                    official = parts[0].replace("OFFICIAL_ANSWER:", "").strip()
                    plain = parts[1].strip()
                else:
                    official = raw_text.strip()
                    plain = self._generate_fallback_plain(query, chunks)

                return {"official_answer": official, "plain_answer": plain}
            except Exception as e:
                logger.warning(f"OpenAI API call failed: {e}")

        # Try Groq API next if available
        if self.groq_client:
            for model_name in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]:
                try:
                    response = self.groq_client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.2,
                        max_tokens=900,
                        timeout=5.0
                    )
                    raw_text = response.choices[0].message.content
                    if "PLAIN_LANGUAGE_ANSWER:" in raw_text:
                        parts = raw_text.split("PLAIN_LANGUAGE_ANSWER:")
                        official = parts[0].replace("OFFICIAL_ANSWER:", "").strip()
                        plain = parts[1].strip()
                    else:
                        official = raw_text.strip()
                        plain = self._generate_fallback_plain(query, chunks)

                    return {"official_answer": official, "plain_answer": plain}
                except Exception as e:
                    logger.warning(f"Groq API model '{model_name}' skipped: {e}")
                    break

        # Instant Grounded Synthesizer Fallback
        return self._generate_fallback_answers(query, chunks)

    def _generate_fallback_plain(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        c = chunks[0]
        return (
            f"• **Main Scheme**: {c['scheme_name']} ({c.get('category', 'Grant/Loan')}).\n"
            f"• **Key Benefit**: Loan/Subsidy limits up to {c.get('max_loan_amount', 'specified limits')} ({c.get('subsidy', 'Govt subvention')}).\n"
            f"• **Target Beneficiaries**: {c.get('target_group', 'Women and MSMEs')} across {c.get('state_or_central', 'India')}."
        )

    def _generate_fallback_answers(self, query: str, chunks: List[Dict[str, Any]]) -> Dict[str, str]:
        """Deterministic grounded fallback when Groq API key is offline or unavailable."""
        query_lower = query.lower()
        domain_keywords = [
            "scheme", "loan", "subsidy", "grant", "eligibility", "women", "business",
            "entrepreneur", "mudra", "stand-up", "pmegp", "udyogini", "pragati", "we hub",
            "msk", "training", "scholarship", "fund", "apply", "tailoring", "store",
            "shop", "interest", "collateral", "bank", "document", "certificate", "age",
            "income", "limit", "gov", "govt", "government", "central", "state", "telangana",
            "karnataka", "andhra", "maharashtra", "startup", "incubation", "seed"
        ]

        is_domain_query = any(k in query_lower for k in domain_keywords)
        
        # Check top chunk score if available
        first_chunk = chunks[0] if chunks else {}
        rrf_score = first_chunk.get("rrf_score", 1.0)
        vector_score = first_chunk.get("vector_score", 1.0)
        bm25_score = first_chunk.get("bm25_score", 1.0)

        if not is_domain_query and first_chunk:
            general_answer = (
                f"Here is information regarding your query on '{query}':\n\n"
                f"To support your entrepreneurial journey, the top government scheme match for your interest is **{first_chunk['scheme_name']}** ({first_chunk['section_title']}):\n"
                f"{first_chunk['text']}\n\n"
                f"**Citations**: [Source: {first_chunk['scheme_name']} - {first_chunk['section_title']}]"
            )
            return {
                "official_answer": general_answer,
                "plain_answer": f"• **Query Assistance**: Provided insights for '{query}'.\n• **Recommended Scheme**: {first_chunk['scheme_name']} offers financial aid up to {first_chunk.get('max_loan_amount', 'specified limits')}.\n• **Next Step**: You can explore eligibility for Mudra, Stand-Up India, PMEGP, or WE Hub grants on the platform."
            }

        official = (
            f"Based on official documents for **{first_chunk['scheme_name']}** ({first_chunk['section_title']}):\n\n"
            f"{first_chunk['text']}\n\n"
            f"**Citations**: [Source: {first_chunk['scheme_name']} - {first_chunk['section_title']}]"
        )
        if len(chunks) > 1:
            second_chunk = chunks[1]
            official += (
                f"\n\nAdditional Details from **{second_chunk['scheme_name']}**:\n"
                f"{second_chunk['text'][:250]}...\n\n"
                f"**Citations**: [Source: {second_chunk['scheme_name']} - {second_chunk['section_title']}]"
            )

        plain = (
            f"• **What it offers**: {first_chunk['scheme_name']} provides financial assistance ({first_chunk.get('max_loan_amount', 'support')}).\n"
            f"• **Who is eligible**: {first_chunk.get('target_group', 'Women and eligible applicants')} in {first_chunk.get('state_or_central', 'India')}.\n"
            f"• **Subsidy benefit**: {first_chunk.get('subsidy', 'Government supported terms')} available upon fulfilling guidelines."
        )

        return {
            "official_answer": official,
            "plain_answer": plain
        }

    def translate_text(self, text: str, target_lang: str) -> str:
        """
        Translates text into Telugu ('te') or Hindi ('hi') using deep-translator.
        Falls back to English text if offline or if translation fails.
        """
        if not text or target_lang.lower() in ["en", "english"]:
            return text

        try:
            from deep_translator import GoogleTranslator
            lang_code = "te" if "telugu" in target_lang.lower() or target_lang == "te" else "hi"
            translator = GoogleTranslator(source="auto", target=lang_code)
            return translator.translate(text)
        except Exception as e:
            logger.warning(f"Translation to {target_lang} failed: {e}. Returning original plain language text.")
            return text

if __name__ == "__main__":
    generator = SchemeAnswerGenerator()
    dummy_chunks = [{
        "scheme_name": "Stand-Up India Scheme",
        "section_title": "Eligibility Criteria",
        "category": "loan",
        "target_group": "women-focused",
        "state_or_central": "Central",
        "max_loan_amount": "Rs. 10 Lakh to Rs. 1 Crore",
        "subsidy": "10-15% Margin Money Convergence",
        "text": "Target Group: SC/ST and/or Woman entrepreneurs above 18 years of age. Enterprise Type: Greenfield enterprises only in manufacturing, services, or trading sector. Borrower should not be in default to any bank."
    }]

    answers = generator.generate_answers("Who can apply for Stand-Up India scheme?", dummy_chunks)
    telugu_translation = generator.translate_text(answers["plain_answer"], "telugu")
    hindi_translation = generator.translate_text(answers["plain_answer"], "hindi")

    print("\n" + "="*70)
    print("            STAGE 9: GROUNDED GENERATION VERIFICATION              ")
    print("="*70)
    print("OFFICIAL ANSWER WITH CITATIONS:")
    print(answers["official_answer"])
    print("-" * 70)
    print("PLAIN LANGUAGE REWRITE (ENGLISH):")
    print(answers["plain_answer"])
    print("-" * 70)
    print("TELUGU TRANSLATION:")
    print(telugu_translation.encode('ascii', errors='backslashreplace').decode('ascii'))
    print("-" * 70)
    print("HINDI TRANSLATION:")
    print(hindi_translation.encode('ascii', errors='backslashreplace').decode('ascii'))
    print("="*70 + "\n")
