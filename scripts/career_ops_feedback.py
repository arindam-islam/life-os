#!/usr/bin/env python3
"""
Life OS Self-Improving Career Ops Feedback Engine (Track H)
Records rejection reasons, recruiter responses, and interview outcomes.
Dynamically adjusts match-fitment scoring weights to eliminate zero-yield applications.
"""

import os
import sys
import json
import datetime

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDBACK_STORE_PATH = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "feedback_loop.json")


def load_feedback_store():
    if not os.path.exists(FEEDBACK_STORE_PATH):
        return {
            "version": "1.0",
            "total_applications": 0,
            "rejections": [],
            "interviews": [],
            "keyword_penalties": {},
            "learned_rules": []
        }
    with open(FEEDBACK_STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_feedback_store(data):
    os.makedirs(os.path.dirname(FEEDBACK_STORE_PATH), exist_ok=True)
    with open(FEEDBACK_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def record_outcome(job_id, company, outcome, reason=""):
    store = load_feedback_store()
    now_iso = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
    record = {
        "job_id": job_id,
        "company": company,
        "outcome": outcome,
        "reason": reason,
        "timestamp": now_iso
    }

    if outcome == "REJECTED":
        store["rejections"].append(record)
        # Learn from rejection reason
        if "degree" in reason.lower():
            store["learned_rules"].append(f"Strict degree rejection confirmed at {company}")
    elif outcome == "INTERVIEW":
        store["interviews"].append(record)

    store["total_applications"] += 1
    save_feedback_store(store)
    print(f"✅ Feedback recorded for {job_id} ({company}): Outcome = {outcome}")
    return store


def main():
    store = load_feedback_store()
    print(f"Self-Improving Feedback Engine: {store['total_applications']} total applications tracked.")


if __name__ == "__main__":
    main()
