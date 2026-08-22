#!/usr/bin/env python3
"""
Life OS Career Ops Tracker & CSV Ledger Sync (Track H)
Maintains structured CSV and JSON job application tracking sheets.
"""

import os
import sys
import json
import csv
import datetime

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOB_LEDGER_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "job_ledger.json")
CSV_TRACKER_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "job_tracker.csv")


def load_ledger():
    if not os.path.exists(JOB_LEDGER_PATH):
        return []
    with open(JOB_LEDGER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ledger(data):
    os.makedirs(os.path.dirname(JOB_LEDGER_PATH), exist_ok=True)
    with open(JOB_LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def export_to_csv():
    ledger = load_ledger()
    fieldnames = [
        "Job ID", "Company", "Role Title", "Domain", "Portal", "Job URL",
        "Offered CTC (LPA)", "Fitment Score", "Status", "Applied Date",
        "Cover Letter Path", "Tailored Resume Path", "Recruiter Contact", "Notes"
    ]

    os.makedirs(os.path.dirname(CSV_TRACKER_PATH), exist_ok=True)
    with open(CSV_TRACKER_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in ledger:
            rec_info = item.get("recruiter_details", {})
            rec_str = f"{rec_info.get('name', 'N/A')} ({rec_info.get('role', 'N/A')})"
            writer.writerow({
                "Job ID": item.get("job_id", ""),
                "Company": item.get("company", ""),
                "Role Title": item.get("title", ""),
                "Domain": item.get("domain", ""),
                "Portal": item.get("portal", ""),
                "Job URL": item.get("url", ""),
                "Offered CTC (LPA)": item.get("offered_ctc_lpa", ""),
                "Fitment Score": item.get("fitment_score", ""),
                "Status": item.get("status", "QUEUED"),
                "Applied Date": item.get("applied_date", ""),
                "Cover Letter Path": item.get("cover_letter_path", ""),
                "Tailored Resume Path": item.get("latex_resume_path", ""),
                "Recruiter Contact": rec_str,
                "Notes": "; ".join(item.get("justification", []))
            })

    print(f"✅ Exported {len(ledger)} job records to CSV tracker: {CSV_TRACKER_PATH}")
    return CSV_TRACKER_PATH


def main():
    export_to_csv()


if __name__ == "__main__":
    main()
