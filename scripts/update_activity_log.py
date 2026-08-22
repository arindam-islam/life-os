#!/usr/bin/env python3
"""
Career Ops Durable Activity Logger (Track H)
Maintains a human-readable Markdown log (.life-os/career_ops/CAREER_OPS_ACTIVITY_LOG.md)
of all job search activities (Discovered, Fitment, Resume/Cover Letter compiled, Pending Video, Applied, Waiting, Rejected, Offer).
"""

import os
import sys
import json
import datetime

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "job_ledger.json")
QUEUE_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "approval_queue.json")
MARKDOWN_LOG_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "CAREER_OPS_ACTIVITY_LOG.md")


def generate_markdown_activity_log():
    jobs = json.load(open(LEDGER_PATH)) if os.path.exists(LEDGER_PATH) else []
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

    content = []
    content.append("# LIFE OS — Career Ops Activity & Application Journal\n")
    content.append(f"> **Last Updated**: `{now_str}`\n")
    content.append("> **Active Strategy**: Target CTC ₹18.0 LPA | Floor ₹16.5 LPA | Location: Bangalore / Remote | Immediate Joiner\n\n")

    content.append("## 📊 Application Pipeline Summary\n")

    # Categorize jobs
    pending_action = [j for j in jobs if j.get("job_id") == "JOB-FULFIL-001" or "PENDING" in str(j.get("status", ""))]
    applied = [j for j in jobs if j.get("status") in ["APPLIED", "SUBMITTED_AND_CONFIRMED"] and j.get("job_id") != "JOB-FULFIL-001"]
    discovered = [j for j in jobs if j.get("status") in ["DISCOVERED", "FITMENT_EVALUATED"]]
    rejected = [j for j in jobs if j.get("status") == "REJECTED"]

    content.append(f"- ⏳ **Pending Action / Video Recording**: `{len(pending_action)}`")
    content.append(f"- 🚀 **Submitted & Waiting for Response**: `{len(applied)}`")
    content.append(f"- 🔍 **Discovered & In Review**: `{len(discovered)}`")
    content.append(f"- ❌ **Rejected / Self-Learned**: `{len(rejected)}`")
    content.append(f"- 💼 **Total Roles Tracked**: `{len(jobs)}`\n\n")

    content.append("---\n")
    content.append("## 📌 Active Job Applications Activity Log\n\n")

    for idx, job in enumerate(jobs, 1):
        job_id = job.get("job_id", f"JOB-{idx:03d}")
        company = job.get("company", "Unknown")
        title = job.get("title", "Unknown")
        ctc = job.get("offered_ctc_lpa", "N/A")
        location = job.get("location", "N/A")
        url = job.get("url", "#")
        status = job.get("status", "DISCOVERED")
        fitment = job.get("fitment_score", "N/A")

        status_emoji = "⏳"
        if "APPLIED" in status or "SUBMITTED" in status:
            status_emoji = "🟢"
        elif "REJECTED" in status:
            status_emoji = "🔴"
        elif "FULFIL" in job_id:
            status_emoji = "🟡"

        content.append(f"### {status_emoji} `{job_id}`: {title} at **{company}**")
        content.append(f"- **Portal / Link**: [{url}]({url})")
        content.append(f"- **Offered CTC**: `{ctc}` | **Location**: `{location}` | **Fitment Match**: `{fitment}`")

        if job_id == "JOB-FULFIL-001":
            content.append(f"- **Current State**: `PAUSED — PENDING VIDEO RECORDING & SLACK REMINDER SET`")
            content.append(f"- **Next Immediate Action**: Record 60-second video answering introduction & 4-step RCA process, attach `.mp4`, click submit.")
            content.append(f"- **Tailored PDF Resume**: [Arindam_Islam_Resume_Fulfil.pdf](file://{WORKSPACE_ROOT}/.life-os/career_ops/pdf_assets/Arindam_Islam_Resume_Fulfil.pdf)")
            content.append(f"- **Tailored PDF Cover Letter**: [Arindam_Islam_Cover_Letter_Fulfil.pdf](file://{WORKSPACE_ROOT}/.life-os/career_ops/pdf_assets/Arindam_Islam_Cover_Letter_Fulfil.pdf)")
            content.append(f"- **Form Proof Screenshot**: [fulfil_form_filled_proof.png](file://{WORKSPACE_ROOT}/.life-os/career_ops/pdf_assets/fulfil_form_filled_proof.png)")
        else:
            content.append(f"- **Current State**: `{status}`")

        content.append("\n---\n")

    with open(MARKDOWN_LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"✅ Updated Markdown activity log: {MARKDOWN_LOG_PATH}")
    return MARKDOWN_LOG_PATH


if __name__ == "__main__":
    generate_markdown_activity_log()
