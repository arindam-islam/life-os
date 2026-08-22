#!/usr/bin/env python3
"""
Life OS — Fix Goals Channel Routing & Delete Erroneous Message
Target Goals Channel: #my-goals (ID: C0BQAPEGADS)
Target Resource Channel: #life-os-resource-inbox (ID: C0BPQBNTK8R)
"""

import urllib.request
import json

SLACK_BOT_TOKEN = "xoxb-11700817286182-11809706620944-iWk9eJ8avcIF3YTWYCmKiEHH"
RESOURCE_CHANNEL = "C0BPQBNTK8R"
MY_GOALS_CHANNEL = "C0BQAPEGADS"
ERRONEOUS_MSG_TS = "1786689774.844649"
USER_TEST_TS = "1786689414.765299"

def delete_erroneous_message():
    url = "https://slack.com/api/chat.delete"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": RESOURCE_CHANNEL,
        "ts": ERRONEOUS_MSG_TS
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"🗑️ Delete erroneous message from resource inbox result: {data}")
    except Exception as e:
        print(f"Error deleting message: {e}")

def reply_to_user_test_in_my_goals():
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }

    reply_text = (
        "🟢 *Life OS Workforce Online!*\n"
        "Received your test signal in <#C0BQAPEGADS> (`#my-goals`).\n"
        "The bot `@n8n-ops-agent` is fully connected to `#my-goals` and ready 24/7 to capture your goals, build action plans, and execute tasks on Oracle VM!"
    )

    payload = {
        "channel": MY_GOALS_CHANNEL,
        "thread_ts": USER_TEST_TS,
        "text": reply_text
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"✅ Reply to user test in #my-goals result: {data.get('ok')}")
    except Exception as e:
        print(f"Error posting reply: {e}")

def post_goal_action_plan_to_my_goals():
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }

    root_payload = {
        "channel": MY_GOALS_CHANNEL,
        "text": "🎯 *New Master Goal Registered:* `GOAL-8833` — *Launch B2B Automation Retainer Service*"
    }
    req_root = urllib.request.Request(url, data=json.dumps(root_payload).encode("utf-8"), headers=headers, method="POST")
    slack_ts = None
    try:
        with urllib.request.urlopen(req_root) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                slack_ts = data.get("ts")
                print(f"✅ Posted root goal message to #my-goals (TS: {slack_ts})")
    except Exception as e:
        print(f"Error posting root goal message: {e}")

    if slack_ts:
        goal_analysis = """🎯 *Life OS Goal Action Plan & Anti-Distraction Safeguard*

📌 *Goal ID:* `GOAL-8833`
📌 *Title:* Launch B2B Automation Retainer Service
📚 *Domain Target:* Artificial Intelligence & Automation -> Software Architecture & Tooling
📂 *Dossier Path:* `.life-os/goals/launch-b2b-automation-retainer-service.md`

⏳ *Estimated Timeline & Milestones:*
• *Estimated Target:* 30 Days from Ingestion
• *Phase 1 (Days 1-7):* Architecture, Schema & Prototype Validation
• *Phase 2 (Days 8-20):* Core Implementation & Automated Testing
• *Phase 3 (Days 21-30):* Production Deployment & KPI Verification

⚡ *Immediate Next 3 Daily Action Items:*
1. Review baseline requirements and define metric boundaries in `.life-os/goals/launch-b2b-automation-retainer-service.md`.
2. Execute initial prototype integration via cloud-hosted subagents on Oracle VM.
3. Validate runtime test pass rate and record progress in Slack thread.

🛡️ *Anti-Distraction & Focus Safeguards:*
• *Single-Lane Invariant:* Do not open secondary feature tracks until Phase 1 milestones pass 100%.
• *Daily Accountability Check:* Reply in this thread every 24h with progress or roadblocks. Life OS will alert you if 48h pass without execution updates.

🎯 *Command Center Instruction:*
Reply directly in this thread with commands like `"Alright let's do it"` or `"Update timeline to 14 days"` to execute next steps autonomously on Oracle VM."""

        thread_payload = {
            "channel": MY_GOALS_CHANNEL,
            "thread_ts": slack_ts,
            "text": goal_analysis
        }
        req_thread = urllib.request.Request(url, data=json.dumps(thread_payload).encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req_thread) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                print(f"✅ Posted threaded goal analysis to #my-goals: {data.get('ok')}")
        except Exception as e:
            print(f"Error posting threaded goal reply: {e}")

if __name__ == "__main__":
    delete_erroneous_message()
    reply_to_user_test_in_my_goals()
    post_goal_action_plan_to_my_goals()
