"""
Stage 8 — Form-Driven Eligibility Checker Engine
Takes structured user profile inputs (age, business stage, applicant category, state)
and evaluates eligibility against scheme metadata to return a shortlisted, ranked list of schemes.
Works directly from form inputs without requiring natural language query entry.
"""

import json
import os
import logging
from pathlib import Path
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class EligibilityChecker:
    def __init__(self, chunks_file: str = None):
        base_dir = Path(__file__).resolve().parent.parent.parent
        if chunks_file is None:
            chunks_file = base_dir / "data" / "processed" / "chunks_with_metadata.json"
        else:
            chunks_file = Path(chunks_file)

        self.chunks = []
        if os.path.exists(chunks_file):
            with open(chunks_file, "r", encoding="utf-8") as f:
                self.chunks = json.load(f)

    def evaluate_profile(
        self,
        age: int = 25,
        business_stage: str = "Idea Stage",
        applicant_category: str = "Women Entrepreneur",
        scheme_type: str = "All",
        state: str = "All India"
    ) -> List[Dict[str, Any]]:
        """
        Evaluates user profile against indexed schemes and returns shortlisted schemes
        with eligibility scores, reasons, and key benefits.
        """
        if not self.chunks:
            logger.warning("No scheme chunks available for eligibility evaluation.")
            return []

        # Group chunks by scheme_name
        schemes_map = {}
        for c in self.chunks:
            sname = c["scheme_name"]
            if sname not in schemes_map:
                schemes_map[sname] = {
                    "scheme_name": sname,
                    "category": c.get("category", "loan"),
                    "target_group": c.get("target_group", "general"),
                    "state_or_central": c.get("state_or_central", "Central"),
                    "max_loan_amount": c.get("max_loan_amount", "N/A"),
                    "subsidy": c.get("subsidy", "N/A"),
                    "chunks": []
                }
            schemes_map[sname]["chunks"].append(c)

        shortlist = []
        for sname, scheme in schemes_map.items():
            score = 50 # Base score
            match_reasons = []
            disqualifiers = []

            # 1. Scheme Category Filter
            if scheme_type != "All":
                type_lower = scheme_type.lower()
                cat_lower = scheme["category"].lower()
                if "loan" in type_lower and cat_lower == "loan":
                    score += 20
                    match_reasons.append("Matches requested Credit/Loan scheme type.")
                elif "scholarship" in type_lower and cat_lower == "scholarship":
                    score += 20
                    match_reasons.append("Matches requested Scholarship program.")
                elif "train" in type_lower and cat_lower == "training":
                    score += 20
                    match_reasons.append("Matches requested Skill Training program.")
                elif "support" in type_lower and cat_lower == "support-service":
                    score += 20
                    match_reasons.append("Matches requested Support Service / Incubation.")

            # 2. Target Group Match (Women / SC-ST / Rural / General)
            target = scheme["target_group"].lower()
            if "women" in applicant_category.lower() or "female" in applicant_category.lower():
                if "women" in target or target == "general" or "female" in target:
                    score += 25
                    match_reasons.append("Women entrepreneurs explicitly targeted or eligible.")
            
            if "sc" in applicant_category.lower() or "st" in applicant_category.lower():
                if "sc" in target or "st" in target:
                    score += 20
                    match_reasons.append("SC/ST special category benefits applicable.")

            if "rural" in applicant_category.lower():
                if "rural" in target:
                    score += 20
                    match_reasons.append("Higher rural subsidy bracket (up to 35%) available.")

            # 3. State vs Central Match
            sch_state = scheme["state_or_central"].lower()
            if sch_state == "central" or sch_state == "national":
                score += 15
                match_reasons.append("Central Government scheme (open nationwide).")
            elif state.lower() in sch_state or sch_state in state.lower():
                score += 25
                match_reasons.append(f"State-specific scheme for {state}.")

            # 4. Age Check Heuristics
            full_text = " ".join([c["text"] for c in scheme["chunks"]]).lower()
            if "minimum 18 years" in full_text or "18 and 55" in full_text or "above 18" in full_text:
                if age >= 18:
                    score += 10
                    match_reasons.append(f"Age {age} meets minimum age requirement (18+).")
                else:
                    disqualifiers.append(f"Age {age} is below minimum required age 18.")

            # Cap score to 100
            score = min(score, 100)

            # Extract eligibility snippet chunk
            eligibility_snippet = "Refer to official scheme document for complete criteria."
            for c in scheme["chunks"]:
                if "eligibility" in c["section_title"].lower() or "criteria" in c["section_title"].lower():
                    eligibility_snippet = c["text"]
                    break

            if score >= 60 and not disqualifiers:
                shortlist.append({
                    "scheme_name": sname,
                    "score": score,
                    "category": scheme["category"],
                    "target_group": scheme["target_group"],
                    "state_or_central": scheme["state_or_central"],
                    "max_loan_amount": scheme["max_loan_amount"],
                    "subsidy": scheme["subsidy"],
                    "match_reasons": match_reasons,
                    "eligibility_snippet": eligibility_snippet
                })

        # Sort shortlist by score descending
        shortlist.sort(key=lambda x: x["score"], reverse=True)
        return shortlist

if __name__ == "__main__":
    checker = EligibilityChecker()
    results = checker.evaluate_profile(
        age=26,
        business_stage="Idea Stage",
        applicant_category="Women Entrepreneur (Rural)",
        scheme_type="Loan / Subsidy",
        state="Telangana"
    )

    print("\n" + "="*70)
    print("           STAGE 8: ELIGIBILITY CHECKER VERIFICATION REPORT        ")
    print("="*70)
    print("Profile Evaluated: 26yo Female | Idea Stage | Rural Women | Telangana")
    print("-" * 70)
    for res in results:
        print(f" • [{res['score']}% Match] {res['scheme_name']}")
        print(f"   Max Loan/Grant: {res['max_loan_amount']} | Subsidy: {res['subsidy']}")
        print(f"   Key Reasons   : {'; '.join(res['match_reasons'][:2])}")
        print("-" * 70)
    print("="*70 + "\n")
