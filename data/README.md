# Nivra Data Directory & Guidelines

This directory manages the document ingestion corpus for Nivra.

## Folder Structure
- `data/raw_pdfs/`: Store original government scheme guidelines in PDF format.
- `data/processed/`: Extracted text `.txt` files and structured chunk output `chunks_with_metadata.json`.
- `data/qdrant_db/`: Local Qdrant vector database persistence folder.

## Official Portal Sources (100+ PDF Corpus Scope)
1. **Stand-Up India**: [standupmitra.in](https://www.standupmitra.in) — Greenfield loans for SC/ST and Women entrepreneurs (Rs. 10 Lakh to Rs. 1 Crore).
2. **Mudra Yojana (PMMY)**: [mudra.org.in](https://www.mudra.org.in) — Micro-business collateral-free loans: Shishu (up to Rs. 50k), Kishore (Rs. 50k to 5L), Tarun (Rs. 5L to 10L).
3. **Ministry of Women & Child Development**: [wcd.nic.in/schemes](https://wcd.nic.in/schemes) — Mahila Shakti Kendra, STEP (Support to Training and Employment Programme for Women).
4. **Women Entrepreneurship Platform (WEP / NITI Aayog)**: [wep.gov.in](https://wep.gov.in) — Incubation, credit access, and mentorship programs.
5. **Ministry of MSME**: [msme.gov.in](https://msme.gov.in) — PMEGP (Prime Minister Employment Generation Programme), TREAD (Trade-Related Entrepreneurship Assistance and Development for Women), Udyogini Scheme, Credit Guarantee Scheme (CGTMSE).
6. **National Scholarship Portal**: [scholarships.gov.in](https://scholarships.gov.in) — Pragati Scholarship for Female Students, Post-Matric and Merit-cum-Means Scholarships.
7. **WE Hub Telangana**: [we-hub.org](https://we-hub.org) — State incubation, seed fund capital, and market linkage grants for women founders in Telangana.
8. **State-Level Welfare Departments**: State MSME portals across Telangana, Andhra Pradesh, Karnataka, Maharashtra, etc.

## Category Coverage
The corpus covers 5 primary categories:
- **Loans & Credit**: Collateral-free loans, interest subvention, working capital support.
- **Subsidies & Grants**: Capital subsidies, margin money support, technology upgrade grants.
- **Skill Training**: Capacity building, vocational training, financial literacy programs.
- **Scholarships**: Financial aid for young women pursuing higher education and technical skills.
- **Support Services**: Incubation, co-working, market linkage, trademark/IP reimbursement.

## File Naming Convention
All raw PDF files in `data/raw_pdfs/` MUST follow lower_snake_case with descriptive scheme names:
- `standup_india_guidelines.pdf`
- `mudra_yojana_scheme.pdf`
- `pmegp_msme_guidelines.pdf`
- `tread_women_entrepreneurs.pdf`
- `udyogini_scheme_guidelines.pdf`
- `we_hub_telangana_grant.pdf`
- `nsp_pragati_scholarship.pdf`
- `mahila_shakti_kendra.pdf`
- `cgtmse_credit_guarantee.pdf`
