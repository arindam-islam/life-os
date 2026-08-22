#!/usr/bin/env python3
"""
Life OS PDF Compiler Engine (Track H)
Generates high-quality, professional single-page PDF resumes & cover letters
with clean candidate file naming (e.g. Arindam_Islam_Resume_Fulfil.pdf).
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "pdf_assets")


def generate_resume_pdf(company_clean, job_title, output_filename):
    os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(PDF_OUTPUT_DIR, output_filename)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor('#1A2B28')
    )

    subhead_style = ParagraphStyle(
        'SubHeadStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#4B5563')
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#7C4DFF'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1F2937')
    )

    story = []

    story.append(Paragraph("ARINDAM ISLAM", header_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Bangalore, India | +91-8553775736 | arindambevan04@gmail.com | linkedin.com/in/arindam-islam", subhead_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D1D5DB'), spaceAfter=8))

    story.append(Paragraph(f"<b>TARGET ROLE:</b> {job_title} at {company_clean}", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>AVAILABILITY:</b> Immediate Joiner (Serving Notice Period Completed — Ready to Join Next Day)", body_style))

    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    summary_text = (
        f"Product & Technical Operations Leader with 7+ years of hands-on experience driving enterprise SaaS, "
        f"smart parking, and micro-mobility operations. Expert in root cause analysis (RCA), Python script reading, "
        f"AI prompt engineering, payment gateway migrations, and no-code/SQL dashboards. Proven track record "
        f"reducing incident resolution times (ART) by 60% and scaling merchant workflows."
    )
    story.append(Paragraph(summary_text, body_style))

    story.append(Paragraph("CORE COMPETENCIES", section_heading))
    skills_text = (
        "Product Operations | Technical Operations | Root Cause Analysis (RCA) | AI & Prompt Engineering | "
        "Metabase SQL | Retool / Appsmith | Python Script Interpretation | Incident Response | SLA Management"
    )
    story.append(Paragraph(skills_text, body_style))

    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))
    exp1 = (
        "<b>Get My Parking (2025 - Present) — Lead - Tech Operations</b><br/>"
        "• Managed 20 Tech Operations & Support Engineers for 60+ enterprise clients across 200+ global sites.<br/>"
        "• Redesigned incident response workflow, reducing Average Resolution Time (ART) from 8+ hrs to ~3 hrs (96%+ efficiency).<br/>"
        "• Spearheaded zero-downtime payment profile migration of 5,000+ customer accounts to Adyen.<br/>"
        "• Implemented MQTT event-based alerting framework and Metabase SQL performance dashboards."
    )
    story.append(Paragraph(exp1, body_style))
    story.append(Spacer(1, 6))

    exp2 = (
        "<b>Bounce (2021 - 2024) — APM & Product Operations</b><br/>"
        "• Defined Battery-as-a-Service (BaaS) subscription roadmap, improving renewal rates from 5% to 30%.<br/>"
        "• Built internal ERP, ticketing, and admin dashboards using Retool/Appsmith, cutting bottlenecks by 25%.<br/>"
        "• Developed GTM strategies and partner payout structures, driving 20% revenue growth in Tier-2/3 expansion."
    )
    story.append(Paragraph(exp2, body_style))

    story.append(Paragraph("EDUCATION", section_heading))
    edu_text = "<b>Technical Diploma in Electronics & Communication Engineering</b> — BSF Institute of Technology, Bangalore (2013 - 2016)<br/><i>Note: 7+ Years Practical Experience Overrides Degree Requirements.</i>"
    story.append(Paragraph(edu_text, body_style))

    doc.build(story)
    print(f"✅ Generated single-page PDF resume: {pdf_path}")
    return pdf_path


def generate_cover_letter_pdf(company_clean, job_title, output_filename):
    os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(PDF_OUTPUT_DIR, output_filename)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#1A2B28'))
    subhead_style = ParagraphStyle('SubHeadStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor('#4B5563'))
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=15, textColor=colors.HexColor('#1F2937'), spaceAfter=10)

    story = []
    story.append(Paragraph("ARINDAM ISLAM", header_style))
    story.append(Paragraph("Bangalore, India | +91-8553775736 | arindambevan04@gmail.com | linkedin.com/in/arindam-islam", subhead_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#D1D5DB'), spaceAfter=14))

    letter_text = (
        f"Dear Hiring Manager at {company_clean},<br/><br/>"
        f"I am writing to express my strong enthusiasm for the <b>{job_title}</b> position at {company_clean}. "
        f"Having spent over 7 years managing high-intensity Product & Technical Operations across enterprise SaaS platforms, "
        f"I thrive as a 'Manager of One' who deep dives into root cause analysis (RCA), interprets Python code, and leverages "
        f"modern AI workflows to solve complex operational challenges.<br/><br/>"
        f"At Get My Parking, I led a team of 20 operations engineers supporting 60+ enterprise clients across 200+ global sites, "
        f"where I reduced Average Resolution Time (ART) from 8+ hours to ~3 hours and executed a zero-downtime migration of 5,000+ "
        f"customer payment profiles to Adyen. Previously at Bounce, I built internal ERP and ticketing workflows using Retool and Appsmith, "
        f"cutting operational bottlenecks by 25%.<br/><br/>"
        f"<b>Availability Notice:</b> My notice period is completed, and I am an <b>Immediate Joiner</b> ready to start the next day once hired.<br/><br/>"
        f"Your high-agency culture, 100% execution efficiency, and AI-integrated mission align perfectly with my technical problem-solving background. "
        f"I am based in Bangalore and fully ready for the role.<br/><br/>"
        f"Best regards,<br/><br/>"
        f"<b>Arindam Islam</b><br/>"
        f"+91-8553775736 | arindambevan04@gmail.com"
    )

    story.append(Paragraph(letter_text, body_style))
    doc.build(story)
    print(f"✅ Generated single-page PDF cover letter: {pdf_path}")
    return pdf_path


def main():
    generate_resume_pdf("Fulfil.IO Inc.", "Product Consultant (Associate) - Supply Chain", "Arindam_Islam_Resume_Fulfil.pdf")
    generate_cover_letter_pdf("Fulfil.IO Inc.", "Product Consultant (Associate) - Supply Chain", "Arindam_Islam_Cover_Letter_Fulfil.pdf")


if __name__ == "__main__":
    main()
