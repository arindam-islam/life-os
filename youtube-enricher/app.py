from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.post("/enrich")
def enrich():
    body = request.get_json(silent=True) or {}
    url = body.get("url")

    if not url:
        return jsonify({"ok": False, "error": "url is required"}), 400

    cmd = [
        "yt-dlp",
        "--dump-single-json",
        "--skip-download",
        "--write-auto-subs",
        "--write-subs",
        "--sub-langs", "en.*",
        url,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=90
        )

        if result.returncode != 0:
            return jsonify({
                "ok": False,
                "error": result.stderr[-3000:]
            }), 502

        data = json.loads(result.stdout)

        return jsonify({
            "ok": True,
            "id": data.get("id"),
            "title": data.get("title"),
            "channel": data.get("channel") or data.get("uploader"),
            "description": data.get("description"),
            "duration": data.get("duration"),
            "upload_date": data.get("upload_date"),
            "webpage_url": data.get("webpage_url"),
            "thumbnail": data.get("thumbnail"),
            "availability": data.get("availability"),
            "live_status": data.get("live_status"),
            "automatic_captions": data.get("automatic_captions"),
            "subtitles": data.get("subtitles"),
        })

    except subprocess.TimeoutExpired:
        return jsonify({"ok": False, "error": "yt-dlp timeout"}), 504
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.get("/health")
def health():
    return jsonify({"ok": True})
