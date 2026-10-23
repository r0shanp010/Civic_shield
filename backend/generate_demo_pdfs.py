import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

demo_dir = r"C:\Users\FIFA 2022\.gemini\antigravity\scratch\civicshield\demo_evidence"
os.makedirs(demo_dir, exist_ok=True)

# Clean existing files in directory
for f in os.listdir(demo_dir):
    try:
        os.remove(os.path.join(demo_dir, f))
    except Exception:
        pass

def create_official_pdf(filename, header_title, subheader, ref_no, date_str, amount_str, facts_list, officer_note):
    filepath = os.path.join(demo_dir, filename)
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        alignment=TA_CENTER
    )
    sub_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#475569'),
        alignment=TA_CENTER
    )
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B')
    )
    bold_style = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0F172A')
    )
    warning_style = ParagraphStyle(
        'WarningStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#991B1B')
    )

    # Header
    story.append(Paragraph(header_title.upper(), title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(subheader, sub_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#2563EB'), spaceAfter=12))

    # Meta Table
    meta_data = [
        [Paragraph('<b>Document Reference:</b> ' + ref_no, meta_style), Paragraph('<b>Date of Incident:</b> ' + date_str, meta_style)],
        [Paragraph('<b>Classification:</b> Verified Evidence Record', meta_style), Paragraph('<b>Amount Involved:</b> ' + amount_str, meta_style)]
    ]
    meta_table = Table(meta_data, colWidths=[260, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Statement of Facts Header
    story.append(Paragraph('STATEMENT OF DOCUMENTED FACTS & EVIDENCE PARTICULARS', bold_style))
    story.append(Spacer(1, 6))

    # Facts Table
    fact_rows = []
    for idx, (lbl, val) in enumerate(facts_list, 1):
        fact_rows.append([Paragraph(f'<b>{idx}. {lbl}</b>', bold_style), Paragraph(val, body_style)])

    fact_table = Table(fact_rows, colWidths=[180, 350])
    fact_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8FAFC')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(fact_table)
    story.append(Spacer(1, 12))

    # Discrepancy / Officer Demand Callout Box
    story.append(Paragraph('VIGILANCE AUDIT / EVIDENCE FINDING NOTE', bold_style))
    story.append(Spacer(1, 4))
    
    note_data = [[Paragraph('<b>[!] AUDIT SUMMARY:</b> ' + officer_note, warning_style)]]
    note_table = Table(note_data, colWidths=[530])
    note_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF2F2')),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#EF4444')),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(note_table)
    story.append(Spacer(1, 15))

    # Verification Footer
    footer_text = Paragraph('<b>Official Seal & Digital Verification Hash:</b> <i>SHA256-AUTHENTICATED-EVIDENCE-CIVICSHIELD</i><br/><font color="#64748B" size="7.5">This digital document is generated for statutory audit and whistleblower grievance examination under Section 7 of the Prevention of Corruption Act.</font>', body_style)
    story.append(footer_text)

    doc.build(story)
    print(f"Generated valid PDF: {filename}")

# 1. BRIBERY
create_official_pdf(
    "1_Bribery_Building_Permit_Challan.pdf",
    "Municipal Corporation — Town Planning & Development Authority",
    "Official Residential Construction Permit Application & Fee Receipt",
    "BP-2026-8812",
    "2026-08-20",
    "Rs. 50,000.00",
    [
        ("Applicant Property Ref", "Plot 44-B, Sector 7, Ward 4, Municipal Limits"),
        ("Application Type", "Residential Building Construction Sanction Order"),
        ("Statutory Challan Paid", "Rs. 3,500/- (Official Govt Treasury Receipt CH-99021)"),
        ("Mandatory Clearances", "Form 7/12 Land Deed, Structural Blueprint, Tax Clearance Approved"),
        ("Action Delayed Since", "2026-06-02 (Pending Senior Inspector Final Signature)")
    ],
    "Senior Town Planning Inspector demanded an unofficial cash payment of Rs. 50,000 in an envelope to release the sanction order. Without payment, the file was threatened with indefinite setback objections."
)

# 2. EXTORTION
create_official_pdf(
    "2_Extortion_Demolition_Threat_Notice.pdf",
    "Town Planning & Municipal Enforcement Division",
    "Immediate Demolition Threat Notice & Site Inspection Report",
    "DEM-EXT-2026-901",
    "2026-08-22",
    "Rs. 30,000.00 / Month",
    [
        ("Commercial Establishment", "Shop No. 12, Commercial Market Complex, Main Bazaar"),
        ("Alleged Infringement", "Purported Setback Margin Deficiency (Unsurveyed)"),
        ("Statutory Trade License", "Valid & Renewed for Financial Year 2026-27"),
        ("Demolition Threat Deadline", "24 Hours from delivery of unnumbered notice")
    ],
    "Assistant Town Inspector explicitly stated that the commercial shopfront demolition drive would be cancelled only if a monthly protection bribe of Rs. 30,000 was delivered in cash to his private agent."
)

# 3. MISUSE OF AUTHORITY
create_official_pdf(
    "3_Misuse_Of_Authority_Vehicle_Logsheet.pdf",
    "Regional Directorate of Public Works & Urban Infrastructure",
    "Official Vehicle Logsheet & Government Fuel Voucher Audit",
    "PWD-VEH-LOG-4402",
    "2026-08-15",
    "Rs. 45,000.00",
    [
        ("Government Vehicle Reg", "KA-01-GA-4402 (Official Utility SUV Scorpio)"),
        ("Assigned Public Officer", "Regional Development Director"),
        ("Unauthorized Kilometers", "850 KM logged for private family vacation trip"),
        ("Government Fuel Coupons", "Rs. 45,000 encashed for unauthorized luxury private cars")
    ],
    "Public Director utilized departmental vehicles and state fuel allowances for personal family travel, while threatening subordinate junior clerks with adverse confidential appraisal reports if they refused domestic chores."
)

# 4. PROCUREMENT CORRUPTION
create_official_pdf(
    "4_Procurement_Rigged_Tender_Audit.pdf",
    "State Highway & Infrastructure Development Corporation",
    "E-Tender Technical Evaluation & Price Rigging Audit Report",
    "HDA-ROAD-2026-09",
    "2026-08-18",
    "Rs. 20,00,000.00",
    [
        ("Public Tender Name", "Ring Road Bypass Bridge Construction & Asphalt Laying"),
        ("Sanctioned Project Cost", "Rs. 20,00,000/- (Twenty Lakhs)"),
        ("Bidding Irregularities", "Confidential technical criteria leaked 48 hours prior to bid closing"),
        ("Favored Contractor Entity", "M/s Horizon Builders (Direct family link to Committee Chairman)")
    ],
    "Lowest eligible bidder (L1) was arbitrarily disqualified on fabricated technical grounds, and the contract was awarded to a favored shell entity at a 40% inflated quotation."
)

# 5. FAVOURITISM
create_official_pdf(
    "5_Favouritism_Faculty_Recruitment_Scorecard.pdf",
    "State University Academic Recruitment Cell",
    "Assistant Professor Selection Committee Interview Merit Scorecard",
    "REC/2026/AP-04",
    "2026-08-14",
    "Non-Monetary (Nepotism)",
    [
        ("Recruitment Post", "Assistant Professor in Computer Applications (MCA Dept)"),
        ("Meritorious Candidate Score", "Academic Score: 89/100, 12 Scopus Papers | Interview: 4/30"),
        ("Selected Candidate Profile", "Academic Score: 42/100, 0 Publications | Interview: 30/30"),
        ("Relationship Disclosed", "Direct family relative of Vice-Chancellor Selection Chair")
    ],
    "Selection committee bypassed UGC mandatory written screening exam and intentionally awarded minimum interview marks to top candidates to appoint an unqualified relative."
)

# 6. FRAUD
create_official_pdf(
    "6_Fraud_Forged_Subsidy_Invoice.pdf",
    "Agricultural Welfare Board & District Treasury",
    "Farm Equipment Subsidy Disbursement & Forgery Audit Report",
    "AG-SUB-2026-771",
    "2026-08-10",
    "Rs. 15,00,000.00",
    [
        ("Welfare Scheme Name", "State Tractor & Agricultural Equipment Subsidy Fund"),
        ("Embezzled Amount", "Rs. 15,00,000/- (Fifteen Lakhs)"),
        ("Fabricated Beneficiaries", "85 Ghost farmer accounts created using forged Aadhaar cards"),
        ("Fund Diversion Channel", "Subsidized machinery payments diverted to private shell bank accounts")
    ],
    "Senior welfare officers generated fictitious invoices and forged verification signatures to siphon Rs. 15 Lakhs of government agricultural subsidies into personal accounts."
)

# 7. ILLEGAL PAYMENT DEMAND
create_official_pdf(
    "7_Illegal_Payment_Hospital_Counter_Receipt.pdf",
    "District Civil Hospital — Healthcare Administration Division",
    "Emergency Maternity Ward Admission Surcharge Incident Log",
    "HOSP-SUR-2026-088",
    "2026-08-28",
    "Rs. 2,500.00",
    [
        ("Healthcare Facility", "District Civil Hospital, Maternity Ward Counter No. 2"),
        ("Statutory Scheme Entitlement", "100% Free Treatment under Janani Shishu Suraksha Scheme"),
        ("Unreceipted Demand", "Rs. 2,500 per patient demanded as unofficial entry surcharge"),
        ("Staff Action", "Admission tokens and delivery ward entry withheld until cash payment")
    ],
    "Billing desk staff demanded mandatory cash surcharges for services legally guaranteed free by the government, refusing patient admission without cash payment."
)

# 8. EMBEZZLEMENT / OTHER
create_official_pdf(
    "8_Embezzlement_Pension_Fund_Diverted_Ledger.pdf",
    "Regional Pension & Provident Fund Directorate",
    "Pension Disbursal Audit & Shadow Account Reconciliation Statement",
    "TR-DIV-2026-449",
    "2026-08-05",
    "Rs. 8,50,000.00",
    [
        ("Audited Department", "Regional Pension & Social Welfare Disbursal Unit"),
        ("Total Diverted Funds", "Rs. 8,50,000/- (Eight Lakh Fifty Thousand)"),
        ("Embezzlement Method", "Unclaimed funds of deceased pensioners routed to shadow account"),
        ("Banking Confirmation", "Systematic monthly ATM cash withdrawals using forged stamps")
    ],
    "Disbursing officer created an unauthorized shadow current account to systematically withdraw and pocket pension allocations of deceased citizens."
)

print("\nSUCCESS: All 8 official PDF evidence files generated in:", demo_dir)
