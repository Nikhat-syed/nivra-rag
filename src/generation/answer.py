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
    def __init__(self, groq_api_key: str = None, model: str = "llama-3.3-70b-versatile"):
        if groq_api_key is None:
            groq_api_key = os.getenv("GROQ_API_KEY", "").strip()

        self.groq_api_key = groq_api_key
        self.model = model
        self.client = None

        if self.groq_api_key and not self.groq_api_key.startswith("your_"):
            try:
                from groq import Groq
                self.client = Groq(api_key=self.groq_api_key)
                logger.info(f"Initialized Groq LLM client with model: {self.model}")
            except Exception as e:
                logger.warning(f"Could not initialize Groq SDK: {e}. Will use grounded fallback synthesizer.")
        else:
            logger.info("No active Groq API Key found. Using deterministic grounded fallback synthesizer.")

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
            "You are Nivra, an official Indian Government Scheme Assistant for women entrepreneurs.\n"
            "CRITICAL RULES:\n"
            "1. Answer the user question STRICTLY using ONLY the official context provided below.\n"
            "2. Do NOT guess, hallucinate, or bring in outside knowledge.\n"
            "3. If the context does not contain enough information, state explicitly: 'I do not have enough official information in the retrieved scheme documents to answer this question.'\n"
            "4. Provide exact citations using format: [Source: Scheme Name - Section Title].\n"
        )

        user_prompt = (
            f"USER QUESTION: {query}\n\n"
            f"RETRIEVED SCHEME CONTEXT:\n{context_str}\n\n"
            "Generate your answer in two sections:\n"
            "OFFICIAL_ANSWER:\n<Official grounded wording with citations>\n\n"
            "PLAIN_LANGUAGE_ANSWER:\n<Simplified 3-bullet point plain English summary for someone with low digital literacy>\n"
        )

        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=900
                )
                raw_text = response.choices[0].message.content
                
                # Parse raw response
                if "PLAIN_LANGUAGE_ANSWER:" in raw_text:
                    parts = raw_text.split("PLAIN_LANGUAGE_ANSWER:")
                    official = parts[0].replace("OFFICIAL_ANSWER:", "").strip()
                    plain = parts[1].strip()
                else:
                    official = raw_text.strip()
                    plain = self._generate_fallback_plain(query, chunks)

                return {
                    "official_answer": official,
                    "plain_answer": plain
                }
            except Exception as e:
                logger.warning(f"Groq API call failed: {e}. Switching to grounded synthesizer fallback.")

        # Grounded Synthesizer Fallback
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
        first_chunk = chunks[0]
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
        Falls back to English text if offline.
        """
        if target_lang.lower() in ["en", "english"]:
            return text

        try:
            from deep_translator import GoogleTranslator
            lang_code = "te" if "telugu" in target_lang.lower() or target_lang == "te" else "hi"
            translator = GoogleTranslator(source="auto", target=lang_code)

            # Split into lines to preserve markdown formatting
            translated_lines = []
            for line in text.splitlines():
                if line.strip():
                    translated_lines.append(translator.translate(line))
                else:
                    translated_lines.append("")
            return "\n".join(translated_lines)
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
