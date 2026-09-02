"""
Stage 10 — Document Checklist Generator
Extracts and structures a clean bullet-point list of required application documents
from retrieved scheme chunks for any selected scheme.
"""

import json
import re
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any

# Ensure UTF-8 stdout for Windows CLI
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class DocumentChecklistGenerator:
    def __init__(self, chunks_file: str = None):
        base_dir = Path(__file__).resolve().parent.parent.parent
        if chunks_file is None:
            chunks_file = base_dir / "data" / "processed" / "chunks_with_metadata.json"
        else:
            chunks_file = Path(chunks_file)

        self.chunks = []
        if Path(chunks_file).exists():
            with open(chunks_file, "r", encoding="utf-8") as f:
                self.chunks = json.load(f)

    def extract_checklist_for_scheme(self, scheme_name: str) -> Dict[str, Any]:
        """
        Scans scheme chunks, locates document requirement sections,
        and parses clean categorized bullet points.
        """
        matching_chunks = [
            c for c in self.chunks
            if scheme_name.lower() in c["scheme_name"].lower() or c["scheme_name"].lower() in scheme_name.lower()
        ]

        if not matching_chunks:
            # Fallback default document checklist
            return {
                "scheme_name": scheme_name,
                "found": False,
                "categories": {
                    "Identity Proof": ["Aadhaar Card", "PAN Card", "Voter ID / Passport"],
                    "Business Documents": ["Business Identity / Udyam Registration", "Trade License"],
                    "Financial & Project": ["Project Report (DPR)", "Bank Statement for last 6 months"],
                    "Category Proof": ["Caste / Income / Rural Certificate (if applicable)"]
                }
            }

        # Search for document chunks
        doc_chunks = [
            c for c in matching_chunks
            if "document" in c["section_title"].lower() or "required" in c["section_title"].lower()
        ]
        if not doc_chunks:
            doc_chunks = matching_chunks

        combined_text = "\n".join([c["text"] for c in doc_chunks])
        
        # Categorized Document Parsers
        identity_docs = []
        business_docs = []
        financial_docs = []
        category_docs = []

        lines = combined_text.splitlines()
        for line in lines:
            line_clean = line.strip(" -*•0123456789.")
            if not line_clean or len(line_clean) < 5:
                continue

            line_lower = line_clean.lower()
            if any(k in line_lower for k in ["aadhaar", "pan", "voter", "passport", "identity", "photo", "residence"]):
                identity_docs.append(line_clean)
            elif any(k in line_lower for k in ["incorporation", "partnership", "registration", "gst", "license", "address proof"]):
                business_docs.append(line_clean)
            elif any(k in line_lower for k in ["project report", "bank statement", "quotation", "balance sheet", "dpr", "financial"]):
                financial_docs.append(line_clean)
            elif any(k in line_lower for k in ["sc/st", "caste", "income", "rural", "training completion"]):
                category_docs.append(line_clean)

        # Ensure sensible fallbacks
        if not identity_docs:
            identity_docs = ["Passport size photographs", "Identity & Residence Proof (Aadhaar / PAN / Voter ID)"]
        if not business_docs:
            business_docs = ["Business Registration / Trade License / Udyam Registration"]
        if not financial_docs:
            financial_docs = ["Detailed Project Report (DPR)", "6-Month Bank Account Statement"]

        return {
            "scheme_name": matching_chunks[0]["scheme_name"],
            "found": True,
            "categories": {
                "Identity & Personal Proof": list(dict.fromkeys(identity_docs)),
                "Entity & Business Documents": list(dict.fromkeys(business_docs)),
                "Financial & Project Reports": list(dict.fromkeys(financial_docs)),
                "Special Category Certificates": list(dict.fromkeys(category_docs)) if category_docs else ["SC/ST or Income Certificate (if applicable)"]
            }
        }

if __name__ == "__main__":
    generator = DocumentChecklistGenerator()
    checklist = generator.extract_checklist_for_scheme("Stand-Up India Scheme")

    print("\n" + "="*70)
    print("         STAGE 10: DOCUMENT CHECKLIST GENERATOR REPORT            ")
    print("="*70)
    print(f"Scheme: {checklist['scheme_name']}")
    print("-" * 70)
    for cat_title, items in checklist["categories"].items():
        print(f"\n{cat_title}:")
        for item in items:
            print(f"  * {item}")
    print("="*70 + "\n")
