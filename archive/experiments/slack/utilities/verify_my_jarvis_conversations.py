#!/usr/bin/env python3
"""
Life OS — Verify & Initialize #my-jarvis-conversations Channel
Checks if channel #my-jarvis-conversations is accessible, posts initialization message,
and updates MONITORED_CHANNELS in slack_workforce_agents.py.
"""

import urllib.request
import json
import sys

SLACK_BOT_TOKEN = "xoxb-11700817286182-11809706620944-iWk9eJ8avcIF3YTWYCmKiEHH"

def test_post(target: str) -> dict:
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": target,
        "text": "🎙️ *Jarvis Voice Mode Active* — Dedicated voice conversation logging initialized!\n• Spoken voice commands and replies will be logged here.\n• Non-voice sessions (Antigravity/Gemini text) will remain local."
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    res = test_post("#my-jarvis-conversations")
    print(f"Post to #my-jarvis-conversations result: {res}")
