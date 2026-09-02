"""
Sample PDF Generator for Nivra
Generates realistic PDF documents for government schemes in data/raw_pdfs/
covering loans, scholarships, skill training, subsidies, and support services.
"""

import os
import sys

def create_sample_pdfs():
    output_dir = os.path.join(os.path.dirname(__file__), "raw_pdfs")
    os.makedirs(output_dir, exist_ok=True)
    
    schemes_data = [
        {
            "filename": "standup_india_guidelines.pdf",
            "title": "Stand-Up India Scheme Guidelines",
            "category": "Loan",
            "target_group": "SC/ST and Women Entrepreneurs",
            "content": """
OFFICIAL GUIDELINES: STAND-UP INDIA SCHEME
Government of India - Department of Financial Services

1. OBJECTIVE
The Stand-Up India Scheme aims to facilitate bank loans between Rs. 10 Lakhs and Rs. 1 Crore to at least one Scheduled Caste (SC) or Scheduled Tribe (ST) borrower and at least one Woman borrower per bank branch for setting up a greenfield enterprise.

2. ELIGIBILITY CRITERIA
- Target Group: SC/ST and/or Woman entrepreneurs above 18 years of age.
- Enterprise Type: Greenfield enterprises only in manufacturing, services, or trading sector.
- Ownership: In case of non-individual entities, 51% of the shareholding and controlling stake must be held by SC/ST or Woman entrepreneur.
- Credit History: Borrower should not be in default to any bank or financial institution.

3. LOAN DETAILS AND SUBSIDY
- Loan Amount: Between Rs. 10 Lakh and Rs. 1 Crore.
- Margin Money: The borrower needs to bring in 15% margin money. Government convergence schemes can contribute up to 10% of project cost.
- Repayment Period: Repayable in 7 years with a maximum moratorium period of 18 months.
- Interest Rate: Lowest applicable rate of the bank for that category (Base Rate / MCLR + 3% + Tenor Premium).

4. DOCUMENTS REQUIRED FOR APPLICATION
- Completed Application Form with passport size photographs.
- Identity Proof: Voter ID / PAN Card / Aadhaar Card / Passport.
- Residence Proof: Recent utility bill / Ration Card / Aadhaar.
- Category Certificate: SC/ST Certificate issued by competent authority (if applicable).
- Business Address Proof & Lease Agreement or Land Ownership Documents.
- Project Report containing financial projections, cash flow analysis, and balance sheet for 3 years.
- Certificate of Incorporation / Partnership Deed / Business Registration Certificate.
- Bank Account Statements for the last 6 months.

5. HOW TO APPLY
Applications can be submitted online via the Stand-Up Mitra portal (www.standupmitra.in) or directly at any Scheduled Commercial Bank branch across India.
"""
        },
        {
            "filename": "mudra_yojana_scheme.pdf",
            "title": "Pradhan Mantri Mudra Yojana (PMMY) Guidelines",
            "category": "Loan",
            "target_group": "Micro-entrepreneurs and Women",
            "content": """
PRADHAN MANTRI MUDRA YOJANA (PMMY)
Micro Units Development & Refinance Agency Ltd. (MUDRA)

1. SCHEME OVERVIEW
Pradhan Mantri MUDRA Yojana provides collateral-free loans up to Rs. 10 Lakhs to non-farm micro and small enterprises.

2. THREE CATEGORIES OF LOANS
- Shishu Loan: Cover loans up to Rs. 50,000 for startup micro-units.
- Kishore Loan: Cover loans above Rs. 50,000 and up to Rs. 5 Lakhs for expanding existing units.
- Tarun Loan: Cover loans above Rs. 5 Lakhs and up to Rs. 10 Lakhs for established business expansion.

3. ELIGIBILITY & TARGET AUDIENCE
- Any Indian citizen who has a business plan for a non-farm revenue-generating activity such as manufacturing, processing, trading, or service sector.
- Special focus on women entrepreneurs, small shopkeepers, artisans, and rural micro-businesses.
- No collateral security or third-party guarantee is required for MUDRA loans.

4. REQUIRED DOCUMENTS
- MUDRA Application Form duly filled.
- Identity Proof: Self-attested copy of Aadhaar Card / PAN / Voter ID.
- Proof of Business Identity: Registration certificate, trade license, GST registration.
- Quotation of machinery or equipment to be purchased.
- Bank statement for last 6 months.
- SC/ST/OBC category proof if claiming targeted sub-limits.

5. APPLICATION PROCESS
Apply through Mudra portal (www.mudra.org.in), UdyamiMitra portal, or any Public/Private Sector Bank, RRB, or MFI.
"""
        },
        {
            "filename": "pmegp_msme_guidelines.pdf",
            "title": "Prime Minister Employment Generation Programme (PMEGP)",
            "category": "Subsidy / Loan",
            "target_group": "General / SC-ST / Women / Rural",
            "content": """
PRIME MINISTER EMPLOYMENT GENERATION PROGRAMME (PMEGP)
Ministry of Micro, Small & Medium Enterprises (KVIC)

1. SCHEME OBJECTIVE
Credit-linked subsidy program to generate self-employment opportunities through establishment of micro-enterprises in non-farm sector.

2. SUBSIDY & FINANCIAL ASSISTANCE
- Maximum Project Cost: Rs. 50 Lakhs for Manufacturing Sector; Rs. 20 Lakhs for Service Sector.
- Subsidy Rates:
  * General Category: 15% (Urban) / 25% (Rural) margin money subsidy.
  * Special Category (Women, SC, ST, OBC, Minorities, Ex-servicemen, PH): 25% (Urban) / 35% (Rural) subsidy.
- Own Contribution: 10% for General; 5% for Special Category/Women.

3. ELIGIBILITY CRITERIA
- Age: Minimum 18 years. No upper age limit.
- Educational Qualification: At least VIII standard pass for projects costing above Rs. 10 Lakhs in manufacturing and above Rs. 5 Lakhs in service sector.
- Existing units or units already taking other Govt subsidies are NOT eligible.

4. REQUIRED DOCUMENTS
- Project Report (DPR) detailing capital expenditure & working capital.
- Educational qualification mark sheet / certificate.
- Caste / Category Certificate (Women applicants enjoy Special Category status).
- Rural Area Certificate from Gram Panchayat / Tehsildar (if claiming rural 35% subsidy).
- Aadhaar Card and PAN Card.
- Entrepreneurship Development Programme (EDP) training completion certificate.

5. HOW TO APPLY
Online application through KVIC PMEGP Portal (www.kviconline.gov.in).
"""
        },
        {
            "filename": "tread_women_entrepreneurs.pdf",
            "title": "Trade Related Entrepreneurship Assistance & Development (TREAD) for Women",
            "category": "Support Service / Subsidy",
            "target_group": "Women Entrepreneurs / Self-Help Groups",
            "content": """
TREAD SCHEME FOR WOMEN ENTREPRENEURS
Ministry of Micro, Small and Medium Enterprises

1. SCHEME OBJECTIVE
To economically empower women in rural and urban areas by providing credit, grant, and training support through Non-Governmental Organizations (NGOs) and Self-Help Groups (SHGs).

2. ASSISTANCE DETAILS
- Government Grant: Up to 30% of total project cost as evaluated by lending institutions.
- Bank Lending: 70% of project cost financed as loan by bank/financial institution.
- Capacity Building: Financial assistance up to Rs. 1 Lakh per batch for training NGOs/SHGs in enterprise management.

3. ELIGIBILITY
- Women entrepreneurs organized under SHGs, Cooperatives, or NGOs.
- Individual women entrepreneurs affiliated with registered non-profit promotion organizations.

4. REQUIRED DOCUMENTS
- NGO / SHG Registration Certificate & Bylaws.
- Audit reports of the promoting organization for past 3 years.
- Detailed list of participating women beneficiaries with Aadhaar details.
- Project proposal with market linkage feasibility study.
"""
        },
        {
            "filename": "udyogini_scheme_guidelines.pdf",
            "title": "Udyogini Scheme Guidelines for Women",
            "category": "Loan / Subsidy",
            "target_group": "Women Entrepreneurs (Rural / Low Income)",
            "content": """
UDYOGINI SCHEME FOR WOMEN ENTREPRENEURS
Karnataka State Women's Development Corporation & Ministry of MSME

1. PURPOSE
Provides subsidized micro-loans to women entrepreneurs in small trades, cottage industries, agriculture, and retail businesses to avoid exploitation by private money lenders.

2. LOAN AMOUNT & SUBSIDY BRACKETS
- Maximum Loan Amount: Up to Rs. 3,00,000 for small business activities.
- Subsidy Rate: 30% subsidy on loan amount for SC/ST and low-income women entrepreneurs.
- Family Income Limit: Family annual income should be less than Rs. 1,50,000 per annum for general category; no income limit for SC/ST women.

3. ELIGIBILITY
- Target Group: Women between 18 and 55 years of age.
- Priority given to widows, destitute women, and disabled women.

4. REQUIRED DOCUMENTS
- Aadhaar Card and Income Certificate.
- Caste Certificate (for SC/ST subsidy benefits).
- Bank Passbook with IFSC code.
- Quotation for tools/equipment to be purchased.
- 2 Passport size photographs.
"""
        },
        {
            "filename": "we_hub_telangana_grant.pdf",
            "title": "WE Hub Telangana Women Entrepreneurship Incubation & Grant Program",
            "category": "Support Service / Training",
            "target_group": "Women-Focused / Telangana Startups",
            "content": """
WE HUB TELANGANA - WOMEN ENTREPRENEURSHIP PLATFORM
Government of Telangana

1. ABOUT WE HUB
WE Hub is India's first state-led incubator for women entrepreneurs, facilitating financial access, incubation, market linkages, and IP/regulatory support.

2. INITIATIVES & SEED FUNDING
- Incubation Cohort: 6 to 12 months customized acceleration for tech, non-tech, and social impact startups.
- Prototype Grant: Seed grants up to Rs. 5 Lakhs for early-stage validation.
- Scaling Capital: Direct access to WE Hub venture partner network & Govt credit guarantee schemes.

3. ELIGIBILITY
- Startups led by female founder(s) holding minimum 51% equity.
- Registered or operating in Telangana state.
- Idea-stage, early-stage, or growth-stage enterprises.

4. REQUIRED DOCUMENTS
- Pitch deck / Business summary.
- Proof of female ownership (Cap table / Certificate of Incorporation).
- Founder's Aadhaar & PAN details.
- Prototype demo link or product description.
"""
        },
        {
            "filename": "nsp_pragati_scholarship.pdf",
            "title": "Pragati Scholarship Scheme for Girl Students (NSP)",
            "category": "Scholarship",
            "target_group": "Women Students / Girl Child",
            "content": """
NATIONAL SCHOLARSHIP PORTAL (NSP)
PRAGATI SCHOLARSHIP SCHEME FOR GIRL STUDENTS (AICTE)

1. SCHEME GOAL
To provide financial encouragement and support to young women pursuing technical education (Diploma and Degree courses).

2. SCHOLARSHIP AMOUNT
- Financial Support: Rs. 50,000 per annum for every year of study (up to 4 years for Degree, 3 years for Diploma).
- Usage: Can be used for college fees, purchase of books, equipment, laptops, and hostel expenses.

3. ELIGIBILITY
- Open ONLY to female students admitted to 1st year of Degree/Diploma course or 2nd year through lateral entry in AICTE approved institutions.
- Maximum 2 girl children per family eligible.
- Family Income: Annual family income must not exceed Rs. 8 Lakhs per annum.

4. DOCUMENTS REQUIRED
- Mark sheet of Class 10th and 12th / ITI.
- Admission letter from AICTE approved degree/diploma college.
- Income Certificate for current financial year issued by competent authority (Tehsildar/SDM).
- Tuition fee receipt paid to college.
- Bank Account details linked with Aadhaar.
- Declaration by parents confirming max 2 girl children in family.
"""
        },
        {
            "filename": "mahila_shakti_kendra.pdf",
            "title": "Mahila Shakti Kendra (MSK) & Skill Training Guidelines",
            "category": "Skill Training / Support Service",
            "target_group": "Rural Women / Self-Help Groups",
            "content": """
MAHILA SHAKTI KENDRA (MSK) SCHEME
Ministry of Women and Child Development

1. OVERVIEW
Mahila Shakti Kendra (MSK) provides an integrated support platform for rural women, offering skill development, digital literacy, health awareness, and micro-enterprise assistance.

2. KEY COMPONENTS & TRAINING
- District Level Centre for Women (DLCW): Training in financial literacy, digital tools, Govt scheme application process.
- Block Level Student Volunteers: Community mobilization and direct door-to-step assistance for women.

3. ELIGIBILITY & BENEFITS
- Rural women, adolescent girls, SHG members across block & gram panchayat levels.
- Free training workshops in stitching, food processing, handicraft production, and digital banking tools.

4. HOW TO REGISTER
Contact local Anganwadi center, Gram Panchayat DLCW coordinator, or District Child Development Project Officer (CDPO).
"""
        }
    ]

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        USE_REPORTLAB = True
    except ImportError:
        USE_REPORTLAB = False

    print(f"Generating sample scheme documents in {output_dir}...")
    for item in schemes_data:
        file_path = os.path.join(output_dir, item["filename"])
        if USE_REPORTLAB:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            title_style = ParagraphStyle(
                'DocTitle',
                parent=styles['Heading1'],
                fontSize=16,
                leading=20,
                textColor='#1E293B',
                spaceAfter=12
            )
            body_style = ParagraphStyle(
                'DocBody',
                parent=styles['Normal'],
                fontSize=10,
                leading=14,
                textColor='#334155',
                spaceAfter=8
            )
            
            story.append(Paragraph(item["title"], title_style))
            story.append(Spacer(1, 10))
            
            for paragraph_text in item["content"].strip().split("\n\n"):
                clean_p = paragraph_text.replace("\n", "<br/>")
                story.append(Paragraph(clean_p, body_style))
                story.append(Spacer(1, 6))
                
            doc.build(story)
        else:
            # Fallback text-based PDF representation or direct file writing
            with open(file_path, "wb") as f:
                header = f"%PDF-1.4\n1 0 obj\n<< /Title ({item['title']}) >>\nendobj\n"
                body = item["content"].encode('utf-8')
                f.write(header.encode('utf-8') + body)
        print(f"  [+] Created: {item['filename']}")

    print(f"Successfully generated sample PDF corpus in {output_dir}")

if __name__ == "__main__":
    create_sample_pdfs()
