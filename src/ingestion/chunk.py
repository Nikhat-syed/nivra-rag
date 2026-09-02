"""
Stage 4 — Semantic Section Chunking with Metadata Enrichment
Splits processed text files into logical section chunks (Eligibility, Loan Details,
Documents Required, How to Apply) and attaches key scheme metadata tags.
Output saved to data/processed/chunks_with_metadata.json.
"""

import os
import json
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Metadata mapping rules for known schemes
METADATA_RULES = {
    "standup_india": {
        "scheme_name": "Stand-Up India Scheme",
        "category": "loan",
        "target_group": "women-focused",
        "state_or_central": "Central",
        "max_loan_amount": "Rs. 1 Crore",
        "subsidy": "10-15% Margin Money Convergence"
    },
    "mudra": {
        "scheme_name": "Pradhan Mantri Mudra Yojana (PMMY)",
        "category": "loan",
        "target_group": "general",
        "state_or_central": "Central",
        "max_loan_amount": "Rs. 10 Lakhs",
        "subsidy": "Collateral-free credit"
    },
    "pmegp": {
        "scheme_name": "Prime Minister Employment Generation Programme (PMEGP)",
        "category": "loan",
        "target_group": "rural",
        "state_or_central": "Central",
        "max_loan_amount": "Rs. 50 Lakhs",
        "subsidy": "15% - 35% Margin Money Subsidy"
    },
    "tread": {
        "scheme_name": "TREAD Scheme for Women Entrepreneurs",
        "category": "support-service",
        "target_group": "women-focused",
        "state_or_central": "Central",
        "max_loan_amount": "70% Bank Credit",
        "subsidy": "30% Govt Grant"
    },
    "udyogini": {
        "scheme_name": "Udyogini Scheme for Women",
        "category": "loan",
        "target_group": "women-focused",
        "state_or_central": "Karnataka",
        "max_loan_amount": "Rs. 3 Lakhs",
        "subsidy": "30% Subsidy for SC/ST/Low Income"
    },
    "we_hub": {
        "scheme_name": "WE Hub Telangana Grant & Incubation",
        "category": "support-service",
        "target_group": "women-focused",
        "state_or_central": "Telangana",
        "max_loan_amount": "Rs. 5 Lakhs Prototype Seed Grant",
        "subsidy": "Incubation & Seed Grant"
    },
    "pragati": {
        "scheme_name": "Pragati Scholarship for Girl Students",
        "category": "scholarship",
        "target_group": "women-focused",
        "state_or_central": "Central",
        "max_loan_amount": "Rs. 50,000 / year",
        "subsidy": "100% Financial Aid"
    },
    "nsp": {
        "scheme_name": "Pragati Scholarship for Girl Students",
        "category": "scholarship",
        "target_group": "women-focused",
        "state_or_central": "Central",
        "max_loan_amount": "Rs. 50,000 / year",
        "subsidy": "100% Financial Aid"
    },
    "mahila_shakti": {
        "scheme_name": "Mahila Shakti Kendra (MSK) Skill Development",
        "category": "training",
        "target_group": "rural",
        "state_or_central": "Central",
        "max_loan_amount": "Free Capacity Building",
        "subsidy": "100% Free Skill Training"
    }
}

def infer_metadata(filename: str, text: str) -> dict:
    """Infer metadata based on filename and content heuristics."""
    filename_lower = filename.lower()
    
    # Check rule base
    for key, meta in METADATA_RULES.items():
        if key in filename_lower:
            return meta.copy()
            
    # Default fallbacks
    category = "support-service"
    if "loan" in text.lower() or "credit" in text.lower():
        category = "loan"
    elif "scholarship" in text.lower() or "stipend" in text.lower():
        category = "scholarship"
    elif "train" in text.lower() or "skill" in text.lower():
        category = "training"

    target = "general"
    if "women" in text.lower() or "girl" in text.lower() or "mahila" in text.lower():
        target = "women-focused"
    elif "sc" in text.lower() or "st" in text.lower():
        target = "SC-ST"
    elif "rural" in text.lower():
        target = "rural"

    state_central = "Central"
    if "telangana" in text.lower() or "we hub" in text.lower():
        state_central = "Telangana"
    elif "karnataka" in text.lower():
        state_central = "Karnataka"

    return {
        "scheme_name": filename.replace("_", " ").replace(".txt", "").title(),
        "category": category,
        "target_group": target,
        "state_or_central": state_central,
        "max_loan_amount": "N/A",
        "subsidy": "N/A"
    }

def split_text_into_sections(text: str) -> list:
    """
    Splits scheme document text into semantic logical sections based on standard section headers.
    """
    # Regex split on numbered headers like "1. OBJECTIVE", "2. ELIGIBILITY", etc.
    header_pattern = r'\n(?=[0-9]+\.\s+[A-Z\s]{3,})'
    raw_sections = re.split(header_pattern, text)
    
    sections = []
    for sec in raw_sections:
        sec_clean = sec.strip()
        if not sec_clean:
            continue
            
        # Determine section title
        lines = sec_clean.splitlines()
        first_line = lines[0].strip()
        
        if re.match(r'^[0-9]+\.\s+', first_line):
            title = re.sub(r'^[0-9]+\.\s+', '', first_line).title()
        elif first_line.isupper() and len(first_line) < 60:
            title = first_line.title()
        else:
            title = "General Information"
            
        sections.append({
            "section_title": title,
            "text": sec_clean
        })
        
    # If no headers detected, split into paragraph blocks
    if len(sections) == 0:
        blocks = [b.strip() for b in text.split("\n\n") if len(b.strip()) > 30]
        for idx, block in enumerate(blocks):
            sections.append({
                "section_title": f"Section {idx+1}",
                "text": block
            })
            
    return sections

def chunk_processed_texts(processed_dir: str = None, output_file: str = None):
    """
    Reads processed txt files, chunks by semantic sections, enriches metadata, and saves JSON.
    """
    base_dir = Path(__file__).resolve().parent.parent.parent
    if processed_dir is None:
        processed_dir = base_dir / "data" / "processed"
    else:
        processed_dir = Path(processed_dir)

    if output_file is None:
        output_file = processed_dir / "chunks_with_metadata.json"
    else:
        output_file = Path(output_file)

    txt_files = list(processed_dir.glob("*.txt"))
    if not txt_files:
        logger.error(f"No processed .txt files found in {processed_dir}. Run extract.py first.")
        return []

    all_chunks = []
    chunk_counter = 0

    for txt_file in txt_files:
        with open(txt_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        meta = infer_metadata(txt_file.name, content)
        sections = split_text_into_sections(content)
        
        for sec in sections:
            chunk_counter += 1
            chunk_data = {
                "chunk_id": f"chunk_{chunk_counter:04d}",
                "source_file": txt_file.name,
                "scheme_name": meta["scheme_name"],
                "category": meta["category"],
                "target_group": meta["target_group"],
                "state_or_central": meta["state_or_central"],
                "max_loan_amount": meta.get("max_loan_amount", "N/A"),
                "subsidy": meta.get("subsidy", "N/A"),
                "section_title": sec["section_title"],
                "text": sec["text"]
            }
            all_chunks.append(chunk_data)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    logger.info(f"Successfully generated {len(all_chunks)} semantic chunks from {len(txt_files)} file(s). Saved to {output_file}")
    
    # Print Chunk Summary Table
    print("\n" + "="*70)
    print("            STAGE 4: SEMANTIC CHUNKING SUMMARY REPORT             ")
    print("="*70)
    print(f"Total Processed Files : {len(txt_files)}")
    print(f"Total Semantic Chunks : {len(all_chunks)}")
    print("-" * 70)
    for c in all_chunks[:8]:
        print(f" [{c['chunk_id']}] {c['scheme_name']:<35} | {c['section_title']:<25} | ({c['category']})")
    if len(all_chunks) > 8:
        print(f" ... and {len(all_chunks) - 8} more chunks.")
    print("="*70 + "\n")

    return all_chunks

if __name__ == "__main__":
    chunk_processed_texts()
