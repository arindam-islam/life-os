#!/usr/bin/env python3
"""
Life OS — Slack Goals Channel Setup & Integration Engine
Creates or maps Slack channel #life-os-goals and links it to .life-os/goals/
"""

import urllib.request
import json
import os

SLACK_BOT_TOKEN = "xoxb-11700817286182-11809706620944-iWk9eJ8avcIF3YTWYCmKiEHH"

def create_or_find_goals_channel():
    # 1. List channels to see if life-os-goals exists
    url = "https://slack.com/api/conversations.list?types=public_channel,private_channel"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            channels = data.get("channels", [])
            for c in channels:
                if c.get("name") in ["life-os-goals", "goals"]:
                    print(f"✅ Found existing Slack Goals Channel: #{c.get('name')} (ID: {c.get('id')})")
                    return c.get("id")
    except Exception as e:
        print(f"Error checking channels: {e}")

    # 2. If not found, create #life-os-goals
    create_url = "https://slack.com/api/conversations.create"
    payload = {"name": "life-os-goals", "is_private": False}
    data_bytes = json.dumps(payload).encode("utf-8")
    headers["Content-Type"] = "application/json; charset=utf-8"

    req_create = urllib.request.Request(create_url, data=data_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req_create) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            if res_data.get("ok"):
                channel_info = res_data.get("channel", {})
                print(f"🎉 Created new Slack channel: #life-os-goals (ID: {channel_info.get('id')})")
                return channel_info.get("id")
            else:
                print(f"Slack channel creation note: {res_data.get('error')}")
    except Exception as e:
        print(f"Exception creating channel: {e}")

    return None

if __name__ == "__main__":
    create_or_find_goals_channel()
