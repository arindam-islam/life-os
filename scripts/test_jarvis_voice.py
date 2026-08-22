#!/usr/bin/env python3
"""
Life OS — High-Definition Iron Man J.A.R.V.I.S. Voice Engine
Uses edge-tts with British Neural Voice (en-GB-RyanNeural) for authentic Paul Bettany J.A.R.V.I.S. tone.
"""

import asyncio
import os
import sys
import subprocess
import edge_tts

JARVIS_VOICE = "en-GB-RyanNeural"
OUTPUT_FILE = "/tmp/jarvis_speech.mp3"

async def generate_jarvis_audio(text: str):
    communicate = edge_tts.Communicate(text, JARVIS_VOICE)
    await communicate.save(OUTPUT_FILE)
    subprocess.run(["afplay", OUTPUT_FILE], check=False)

def speak_jarvis(text: str):
    try:
        asyncio.run(generate_jarvis_audio(text))
    except Exception as e:
        print(f"Fallback to native voice due to: {e}")
        subprocess.run(["say", "-v", "Daniel", text], check=False)

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Always at your service, Boss."
    speak_jarvis(msg)
