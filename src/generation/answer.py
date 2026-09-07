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
        Answers every user question (general entrepreneurship advice + scheme grounded).
        """
        context_str = self.format_context_prompt(chunks) if chunks else "No specific matching scheme documents retrieved."

        system_prompt = (
            "You are Nivra, an expert AI advisor empowering women entrepreneurs in India.\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. Answer EVERY single user question directly, accurately, and comprehensively.\n"
            "2. If the user asks a general business, marketing, financial, or operational question, provide top-tier practical advice first, then connect it to relevant Indian government schemes.\n"
            "3. When scheme context is present, cite specific schemes accurately using: [Source: Scheme Name - Section Title].\n"
        )

        user_prompt = (
            f"USER QUESTION: {query}\n\n"
            f"RETRIEVED SCHEME CONTEXT:\n{context_str}\n\n"
            "Generate your answer in two sections:\n"
            "OFFICIAL_ANSWER:\n<Detailed comprehensive answer with step-by-step guidance and citations>\n\n"
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
                    temperature=0.3,
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
                logger.warning(f"OpenAI API call failed ({e}). Attempting next model provider...")

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
                        temperature=0.3,
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

        # Instant Grounded & Structured Synthesizer Fallback
        return self._generate_fallback_answers(query, chunks)

    def _generate_fallback_plain(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        if chunks:
            c = chunks[0]
            s_name = c.get('scheme_name', 'Government Scheme')
            s_cat = c.get('category', 'Financial Aid')
            s_max = c.get('max_loan_amount', 'specified limits')
            s_tgt = c.get('target_group', 'Women Entrepreneurs')
            s_loc = c.get('state_or_central', 'India')
            return (
                f"• **Main Scheme**: {s_name} ({s_cat}).\n"
                f"• **Key Benefit**: Loan/Subsidy limits up to {s_max}.\n"
                f"• **Target Beneficiaries**: {s_tgt} across {s_loc}."
            )
        return (
            f"• **Query Addressed**: Provided business & scheme guidance for '{query}'.\n"
            "• **Recommended Financial Options**: Explore Mudra Loans (up to Rs. 10 Lakhs) and Stand-Up India (up to Rs. 1 Crore).\n"
            "• **Next Steps**: Check eligibility and required document checklists on the Nivra platform."
        )

    def _generate_fallback_answers(self, query: str, chunks: List[Dict[str, Any]]) -> Dict[str, str]:
        """Fail-safe grounded synthesizer answering all queries safely."""
        if chunks:
            first_chunk = chunks[0]
            scheme_name = first_chunk.get("scheme_name", "Government Scheme")
            section_title = first_chunk.get("section_title", "Details")
            text_snippet = first_chunk.get("text", "Official scheme guidelines available.")
            max_loan = first_chunk.get("max_loan_amount", "financial assistance")
            target_group = first_chunk.get("target_group", "Women Entrepreneurs")
            state_loc = first_chunk.get("state_or_central", "India")
            subsidy = first_chunk.get("subsidy", "Government subvention")

            official = (
                f"### Business & Scheme Guidance for '{query}'\n\n"
                f"Based on official documents for **{scheme_name}** ({section_title}):\n\n"
                f"{text_snippet}\n\n"
                f"**Citations**: [Source: {scheme_name} - {section_title}]"
            )
            if len(chunks) > 1:
                second_chunk = chunks[1]
                s2_name = second_chunk.get("scheme_name", "Support Scheme")
                s2_title = second_chunk.get("section_title", "Additional Info")
                s2_text = second_chunk.get("text", "")[:250]
                official += (
                    f"\n\nAdditional Details from **{s2_name}**:\n"
                    f"{s2_text}...\n\n"
                    f"**Citations**: [Source: {s2_name} - {s2_title}]"
                )

            plain = (
                f"• **What it offers**: {scheme_name} provides {max_loan}.\n"
                f"• **Who is eligible**: {target_group} in {state_loc}.\n"
                f"• **Subsidy benefit**: {subsidy} upon fulfilling official criteria."
            )
            return {"official_answer": official, "plain_answer": plain}

        # Fallback for general questions when no specific scheme chunks matched
        official = (
            f"### Entrepreneurship & Strategic Guidance for '{query}'\n\n"
            f"To successfully execute your request regarding **'{query}'**, consider these key steps:\n\n"
            "1. **Market Planning & Feasibility**: Conduct local market research, define your target audience, and establish competitive pricing.\n"
            "2. **Financial Assistance & Capital**: You can apply for government loans tailored for women entrepreneurs, such as:\n"
            "   - **Pradhan Mantri Mudra Yojana (PMMY)**: Collateral-free loans up to Rs. 10 Lakhs (Shishu, Kishore, Tarun).\n"
            "   - **Stand-Up India**: Bank loans between Rs. 10 Lakhs and Rs. 1 Crore with up to 15% margin money convergence.\n"
            "   - **Udyogini Scheme**: Subsidized micro-loans up to Rs. 3 Lakhs with 30% subsidy for eligible women.\n"
            "3. **Skill & Support Infrastructure**: Leverage incubation hubs (like WE Hub) and MSME training programs for technical and digital marketing support.\n"
        )
        plain = (
            f"• **Action Plan**: Detailed roadmap prepared for '{query}'.\n"
            "• **Funding Options**: Mudra Loans (up to 10L), Stand-Up India (up to 1 Cr), and Udyogini (30% subsidy).\n"
            "• **Next Steps**: Use the Eligibility Checker tab to see which scheme best fits your age and stage."
        )
        return {"official_answer": official, "plain_answer": plain}


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
