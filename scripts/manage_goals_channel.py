#!/usr/bin/env python3
"""
Life OS — Delete Test Goal Message & Setup Dedicated 'my-goals' Channel
"""

import urllib.request
import json

SLACK_BOT_TOKEN = "xoxb-11700817286182-11809706620944-iWk9eJ8avcIF3YTWYCmKiEHH"
RESOURCE_CHANNEL = "C0BPQBNTK8R"
TEST_MSG_TS = "1786688833.727189"

def delete_test_message():
    url = "https://slack.com/api/chat.delete"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": RESOURCE_CHANNEL,
        "ts": TEST_MSG_TS
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"🗑️ Delete test message result: {data}")
    except Exception as e:
        print(f"Error deleting message: {e}")

def create_or_get_my_goals_channel():
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }

    # 1. Try creating 'my-goals'
    url_create = "https://slack.com/api/conversations.create"
    payload = {"name": "my-goals", "is_private": False}
    req = urllib.request.Request(url_create, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")

    channel_id = None
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                channel_info = data.get("channel", {})
                channel_id = channel_info.get("id")
                print(f"🎉 Created channel 'my-goals' (ID: {channel_id})")
            else:
                print(f"Channel create status: {data.get('error')}")
    except Exception as e:
        print(f"Error creating channel: {e}")

    # 2. If creation returned error/name_taken or missing_scope, search public channels
    if not channel_id:
        url_list = "https://slack.com/api/conversations.list?types=public_channel,private_channel"
        req_list = urllib.request.Request(url_list, headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}, method="GET")
        try:
            with urllib.request.urlopen(req_list) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for c in data.get("channels", []):
                    if c.get("name") in ["my-goals", "goals", "life-os-goals"]:
                        channel_id = c.get("id")
                        print(f"✅ Found channel #{c.get('name')} (ID: {channel_id})")
                        break
        except Exception as e:
            print(f"Error listing channels: {e}")

    # 3. Join the channel if found
    if channel_id:
        url_join = "https://slack.com/api/conversations.join"
        req_join = urllib.request.Request(url_join, data=json.dumps({"channel": channel_id}).encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req_join) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                print(f"Joined channel result: {data.get('ok')}")
        except Exception as e:
            pass

    return channel_id

def post_goal_to_channel(channel_id):
    if not channel_id:
        channel_id = RESOURCE_CHANNEL # fallback

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }

    # Root message
    root_payload = {
        "channel": channel_id,
        "text": "🎯 *New Master Goal Registered:* `GOAL-8833` — *Launch B2B Automation Retainer Service*"
    }
    req_root = urllib.request.Request(url, data=json.dumps(root_payload).encode("utf-8"), headers=headers, method="POST")
    slack_ts = None
    try:
        with urllib.request.urlopen(req_root) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                slack_ts = data.get("ts")
                print(f"✅ Posted root goal message to channel {channel_id} (TS: {slack_ts})")
    except Exception as e:
        print(f"Error posting root goal message: {e}")

    # Threaded analysis reply
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
            "channel": channel_id,
            "thread_ts": slack_ts,
            "text": goal_analysis
        }
        req_thread = urllib.request.Request(url, data=json.dumps(thread_payload).encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req_thread) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                print(f"✅ Posted threaded goal analysis to channel {channel_id}: {data.get('ok')}")
        except Exception as e:
            print(f"Error posting threaded goal reply: {e}")

if __name__ == "__main__":
    delete_test_message()
    cid = create_or_get_my_goals_channel()
    post_goal_to_channel(cid)
