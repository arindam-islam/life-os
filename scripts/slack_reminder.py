#!/usr/bin/env python3
"""
Slack Reminder Engine for Life OS (Track B & Track H)
Target Channel: #career-ops-inbox
Includes full video scripts and action guides in Slack payloads.
"""

import os
import sys
import json
import datetime
import urllib.request

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(WORKSPACE_ROOT, ".env")
SLACK_REMINDER_LOG = os.path.join(WORKSPACE_ROOT, ".life-os", "career_ops", "slack_reminders.json")

FULFIL_VIDEO_SCRIPT = """🎥 *FULFIL.IO VIDEO RECORDING SCRIPT (Product Consultant)*

> *Read this script directly off your phone screen while recording your video!*

"Hi team! I'm Arindam Islam, based in Bangalore.

Over the past 7+ years, I’ve led Product & Technical Operations across high-volume platforms like Get My Parking and Bounce. I’ve managed teams of 20+ operations engineers, built internal admin/ERP tools using Retool and Appsmith, and scaled merchant operations supporting over 200 global sites.

I’m drawn to Fulfil because of your high-agency culture and your mission to build an AI-integrated ERP for e-commerce brands. I operate best as a 'Manager of One' who takes total ownership—bridging deep technical RCA with merchant success.

When I encounter a complex problem where I don't know the answer, my default next move is a structured 4-step framework:

1. *Root Cause Isolation:* I dive straight into the raw data—reading underlying Python code, inspecting API request logs, or running Metabase SQL queries.
2. *Leverage AI & System Context:* I use AI tools to parse stack traces, cross-reference documentation, and form clear hypotheses.
3. *Methodical Testing:* I test assumptions in a sandbox environment, systematically isolating variables until I hit the exact failure point.
4. *Solve & Standardize:* Once fixed, I write a clear RCA and build a reusable Knowledge Base guide so the team never has to solve the exact same problem twice.

Thank you, and I look forward to connecting!"
"""


def get_career_ops_webhook_url():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("SLACK_CAREER_OPS_WEBHOOK_URL="):
                    return line.strip().split("=", 1)[1]
    return os.environ.get("SLACK_CAREER_OPS_WEBHOOK_URL", "")


def send_slack_reminder(reminder_title, reminder_body, include_script=True):
    webhook_url = get_career_ops_webhook_url()

    message_text = f"🎬 *CAREER OPS REMINDER — {reminder_title}*\n\n{reminder_body}"
    if include_script:
        message_text += f"\n\n{FULFIL_VIDEO_SCRIPT}"

    payload = {"text": message_text}

    status_str = "LOGGED_LOCAL_DESK_JOURNAL (#career-ops-inbox)"
    if webhook_url:
        try:
            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            res = urllib.request.urlopen(req, timeout=10)
            if res.getcode() == 200:
                status_str = "DISPATCHED_TO_SLACK_CAREER_OPS_INBOX"
        except Exception as e:
            status_str = f"DESK_LOGGED (Network) — {str(e)}"

    record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "title": reminder_title,
        "body": reminder_body,
        "script_included": include_script,
        "status": status_str,
        "channel": "#career-ops-inbox"
    }

    reminders = json.load(open(SLACK_REMINDER_LOG)) if os.path.exists(SLACK_REMINDER_LOG) else []
    reminders.insert(0, record)
    with open(SLACK_REMINDER_LOG, "w", encoding="utf-8") as f:
        json.dump(reminders, f, indent=2)

    print(f"🔔 [Career Ops Reminder Dispatch] Channel: #career-ops-inbox | Status: {status_str}")
    return record


if __name__ == "__main__":
    send_slack_reminder(
        "Fulfil.io Video Recording Script Ready",
        "Hey Arindam! Below is your complete teleprompter script for your 60-second video:"
    )
