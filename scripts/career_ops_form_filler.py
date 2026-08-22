#!/usr/bin/env python3
"""
Life OS Automated Form Filler & Recruiter Email Outreach Engine
"""

import os
import json


WORKSPACE_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

PROFILE_PATH = os.path.join(
    WORKSPACE_ROOT,
    ".life-os",
    "career_ops",
    "candidate_profile.json"
)

OUTREACH_DIR = os.path.join(
    WORKSPACE_ROOT,
    ".life-os",
    "career_ops",
    "outreach"
)


def load_profile():
    if not os.path.exists(PROFILE_PATH):
        return {}

    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("candidate", {})


def get_application_form_payload(job):
    profile = load_profile()

    return {
        "full_name": profile.get("name", "Arindam Islam"),
        "email": profile.get("email", "arindambevan04@gmail.com"),
        "phone": profile.get("phone", "+91-8553775736"),
        "current_location": "Bangalore, India",
        "total_experience_years": 7.0,
        "current_designation": "Lead - Tech Operations",
        "expected_ctc_lpa": 18.0,
	"min_ctc_lpa_floor": 16.5,
        "job_id": job.get("job_id"),
        "company": job.get("company"),
        "title": job.get("title"),
    }


def generate_recruiter_email_draft(job):
    payload = get_application_form_payload(job)

    draft = f"""
Subject: Application: {payload['title']} - Arindam Islam

Dear Hiring Team,

I am applying for the {payload['title']} role at {payload['company']}.

I bring 7+ years of experience across Product Operations and Tech Operations.

Best regards,
Arindam Islam
"""

    os.makedirs(OUTREACH_DIR, exist_ok=True)

    file_path = os.path.join(
        OUTREACH_DIR,
        f"email_draft_{job.get('job_id')}.txt"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(draft)

    return file_path, draft
