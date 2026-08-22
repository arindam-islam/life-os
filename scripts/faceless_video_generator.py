#!/usr/bin/env python3
"""
Life OS — Autonomous Faceless AI Video & Reels Generator Engine
Generates 9:16 (vertical reels/shorts) and 16:9 tech/product videos using FFmpeg, TTS, SRT subtitles, and glassmorphic branding.
"""

import os
import sys
import json
import argparse
import subprocess
import wave
import math
from pathlib import Path

DEFAULT_VERTICAL_RES = (1080, 1920)
DEFAULT_HORIZONTAL_RES = (1920, 1080)


def generate_video_script(topic: str, duration_sec: float = 30.0) -> dict:
    """
    Generates structured script with hook, main points, CTA, and timed segments.
    """
    cleaned_topic = topic.strip() or "Productivity & AI Hacks"

    segments = [
        {
            "id": 1,
            "type": "HOOK",
            "text": f"Stop scrolling! Here is how {cleaned_topic} changes everything.",
            "start": 0.0,
            "end": 5.0
        },
        {
            "id": 2,
            "type": "POINT_1",
            "text": "First, automation eliminates repetitive manual tasks and saves hours daily.",
            "start": 5.0,
            "end": 12.0
        },
        {
            "id": 3,
            "type": "POINT_2",
            "text": "Second, AI content pipelines scale your brand at zero additional cost.",
            "start": 12.0,
            "end": 20.0
        },
        {
            "id": 4,
            "type": "POINT_3",
            "text": "Third, autonomous workflows run 24/7 so you focus on high-value strategy.",
            "start": 20.0,
            "end": 26.0
        },
        {
            "id": 5,
            "type": "CTA",
            "text": "Follow Life OS and visit arindamislam.duckdns.org for full details!",
            "start": 26.0,
            "end": max(duration_sec, 30.0)
        }
    ]

    full_speech = " ".join([seg["text"] for seg in segments])
    return {
        "topic": cleaned_topic,
        "duration": max(duration_sec, 30.0),
        "full_text": full_speech,
        "segments": segments
    }


def format_srt_time(seconds: float) -> str:
    """Format seconds into SRT timestamp string: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        millis = 999
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def create_srt_file(segments: list, output_srt_path: str) -> str:
    """Creates an SRT subtitle file from timed script segments."""
    srt_lines = []
    for seg in segments:
        start_str = format_srt_time(seg["start"])
        end_str = format_srt_time(seg["end"])
        srt_lines.append(f"{seg['id']}")
        srt_lines.append(f"{start_str} --> {end_str}")
        srt_lines.append(f"{seg['text']}")
        srt_lines.append("")

    content = "\n".join(srt_lines)
    Path(output_srt_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_srt_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_srt_path


def synthesize_audio(text: str, output_audio_path: str) -> str:
    """
    Synthesizes speech narration.
    Uses macOS `/usr/bin/say` if available, or falls back to WAV wave file creation.
    """
    Path(output_audio_path).parent.mkdir(parents=True, exist_ok=True)

    # Try macOS say command
    say_bin = "/usr/bin/say"
    if os.path.exists(say_bin):
        try:
            cmd = [say_bin, "-o", output_audio_path, "--data-format=LEI16@22050", text]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if os.path.exists(output_audio_path) and os.path.getsize(output_audio_path) > 0:
                return output_audio_path
        except Exception:
            pass

    # Fallback: Create silent/synthetic WAV file
    duration_sec = max(len(text) * 0.08, 10.0)
    sample_rate = 22050
    num_samples = int(sample_rate * duration_sec)

    with wave.open(output_audio_path, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        # Generate subtle 440Hz tone with low amplitude
        raw_data = bytearray()
        for i in range(num_samples):
            value = int(1000 * math.sin(2 * math.pi * 440 * i / sample_rate))
            raw_data.extend(value.to_bytes(2, byteorder='little', signed=True))
        wav_file.writeframes(raw_data)

    return output_audio_path


def build_ffmpeg_command(audio_path: str, srt_path: str, output_video_path: str, aspect: str = "9:16", duration: float = 30.0) -> list:
    """
    Constructs the FFmpeg command line string for rendering the video canvas, subtitles, and audio track.
    """
    width, height = DEFAULT_VERTICAL_RES if aspect == "9:16" else DEFAULT_HORIZONTAL_RES

    # Escape SRT path for ffmpeg filter
    escaped_srt = srt_path.replace(":", "\\:").replace("'", "'\\''")

    filter_graph = (
        f"testsrc2=size={width}x{height}:rate=30,format=yuv420p[bg];"
        f"[bg]drawtext=text='LIFE OS AI ENGINE':fontcolor=white@0.9:fontsize=36:x=(w-text_w)/2:y=80[header];"
        f"[header]subtitles='{escaped_srt}':force_style='FontSize=24,PrimaryColour=&H00FFFFFF,BackColour=&H80000000,BorderStyle=4,Alignment=2'[outv]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=0x0a0f1d:s={width}x{height}:d={duration}:r=30",
        "-i", audio_path,
        "-vf", filter_graph,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        output_video_path
    ]
    return cmd


def render_faceless_video(topic: str, aspect: str = "9:16", duration: float = 30.0, output_path: str = "output_reel.mp4", dry_run: bool = False) -> dict:
    """
    Main orchestration entrypoint for Faceless AI Video rendering.
    """
    script_data = generate_video_script(topic, duration)

    base_dir = Path(output_path).parent
    base_name = Path(output_path).stem

    audio_path = str(base_dir / f"{base_name}_audio.wav")
    srt_path = str(base_dir / f"{base_name}_subtitles.srt")

    create_srt_file(script_data["segments"], srt_path)
    synthesize_audio(script_data["full_text"], audio_path)

    ffmpeg_cmd = build_ffmpeg_command(audio_path, srt_path, output_path, aspect, script_data["duration"])

    result = {
        "status": "SUCCESS",
        "topic": topic,
        "aspect": aspect,
        "duration": script_data["duration"],
        "audio_path": audio_path,
        "srt_path": srt_path,
        "output_path": output_path,
        "script": script_data,
        "ffmpeg_cmd": " ".join(ffmpeg_cmd),
        "rendered": False
    }

    if not dry_run:
        # Check if ffmpeg exists
        ffmpeg_bin = "ffmpeg"
        try:
            subprocess.run([ffmpeg_bin, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            result["rendered"] = True
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            result["status"] = "FFMPEG_UNAVAILABLE_OR_FAILED"
            result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(description="Life OS Autonomous Faceless AI Video & Reels Generator Engine")
    parser.add_argument("--topic", type=str, default="3 AI Hacks for Productivity", help="Topic or prompt for the video")
    parser.add_argument("--aspect", type=str, choices=["9:16", "16:9"], default="9:16", help="Aspect ratio (9:16 vertical reels or 16:9 horizontal)")
    parser.add_argument("--duration", type=float, default=30.0, help="Target duration in seconds")
    parser.add_argument("--output", type=str, default="output_reel.mp4", help="Output MP4 file path")
    parser.add_argument("--dry-run", action="store_true", help="Generate script, SRT, audio, and ffmpeg command without calling ffmpeg")

    args = parser.parse_args()
    res = render_faceless_video(
        topic=args.topic,
        aspect=args.aspect,
        duration=args.duration,
        output_path=args.output,
        dry_run=args.dry_run
    )
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
