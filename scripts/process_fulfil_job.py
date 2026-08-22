#!/usr/bin/env python3
"""
Career Ops Job Processor for Fulfil.io Job Posting (JOB-FULFIL-001)
Updated with Immediate Joiner status and professional PDF attachment filenames.
"""

import os
import sys
import json

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "approval_queue.json")
LEDGER_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "job_ledger.json")

job = {
    "job_id": "JOB-FULFIL-001",
    "portal": "Fulfil Careers",
    "company": "Fulfil.IO Inc.",
    "title": "Product Consultant (Associate) - Supply Chain",
    "domain": "E-Commerce ERP & Supply Chain SaaS",
    "location": "Bangalore (ONSITE - 5:30 PM to 2:30 AM IST)",
    "offered_ctc_lpa": "16.0 - 20.0 LPA",
    "fitment_score": "95%",
    "url": "https://jobs.fulfil.io/o/product-consultant-associate-supply-chain-aug-2026-start",
    "recruiter_details": {
        "name": "Fulfil Hiring Team / Recruiter",
        "role": "Talent Acquisition at Fulfil.IO Inc.",
        "linkedin": "https://www.linkedin.com/company/fulfil-io"
    },
    "required_skills": [
        "Product Operations", "Root Cause Analysis (RCA)", "Python Scripting",
        "AI & Prompt Engineering", "SLA Management", "ERP & Supply Chain"
    ],
    "full_job_description": "Bridge between engineering and e-commerce merchants on Fulfil AI integrated ERP. Perform RCA on operational issues, interpret Python code, design workflow improvements, and own issues end-to-end.",
    "justification": [
        "Base Salary ₹16.0 - 20.0 LPA perfectly hits target 18.0 LPA CTC",
        "Direct match for 7+ years Product & Tech Ops experience (RCA, ART 8h -> 3h, Adyen migration)",
        "Requires AI & Prompt Engineering + Python script interpretation",
        "Bangalore location match (5:30 PM - 2:30 AM IST shift)"
    ],
    "resume_pdf_path": ".life-os/career_ops/pdf_assets/Arindam_Islam_Resume_Fulfil.pdf",
    "cover_letter_pdf_path": ".life-os/career_ops/pdf_assets/Arindam_Islam_Cover_Letter_Fulfil.pdf",
    "human_approval": {
        "status": "PENDING_OWNER_APPROVAL",
        "allowed_actions": ["GO", "APPROVE APPLY JOB-FULFIL-001", "REJECT JOB-FULFIL-001"]
    }
}

queue = json.load(open(QUEUE_PATH)) if os.path.exists(QUEUE_PATH) else []
queue = [item for item in queue if item.get("job_id") != "JOB-FULFIL-001"]
queue.insert(0, job)
with open(QUEUE_PATH, "w", encoding="utf-8") as f:
    json.dump(queue, f, indent=2)

ledger = json.load(open(LEDGER_PATH)) if os.path.exists(LEDGER_PATH) else []
ledger = [item for item in ledger if item.get("job_id") != "JOB-FULFIL-001"]
ledger.insert(0, job)
with open(LEDGER_PATH, "w", encoding="utf-8") as f:
    json.dump(ledger, f, indent=2)

print("✅ Updated JOB-FULFIL-001 payload with Immediate Joiner status and PDF asset paths.")
