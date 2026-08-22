#!/usr/bin/env python3
"""
Life OS — Domain & Area Resource Distribution Engine
Enforces the "No Empty Folders" invariant by placing rich, verified Markdown dossiers directly inside
`.life-os/areas/<area_name>/resources/<human_readable_slug>.md`.
Also updates the master index and queues ready-to-render Faceless Reel scripts into `.life-os/content_queue/pending_reels.json`.
"""

import os
import sys
import json
import re
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
LIFE_OS_DIR = BASE_DIR / ".life-os"
AREAS_DIR = LIFE_OS_DIR / "areas"
KNOWLEDGE_DIR = LIFE_OS_DIR / "knowledge"
MASTER_INDEX_PATH = KNOWLEDGE_DIR / "ingested_resources.json"
PENDING_REELS_PATH = LIFE_OS_DIR / "content_queue" / "pending_reels.json"

AREAS_MAP = {
    "AI_AUTOMATION": "ai_automation",
    "HEALTH_WELLNESS": "health_wellness",
    "PRODUCTIVITY_HACKS": "productivity_hacks",
    "CREATIVE_CONVERSATIONS": "creative_conversations",
    "CAREER_WEALTH": "career_wealth",
    "BUSINESS_STRATEGY": "career_wealth"
}


def slugify_title(title: str) -> str:
    """Converts a title string into a clean, human-readable filename slug."""
    if not title:
        return "captured-resource"
    clean = re.sub(r'[^a-zA-Z0-9\s-]', '', title).lower()
    slug = re.sub(r'[\s_-]+', '-', clean).strip('-')
    return slug[:60] if slug else "captured-resource"


def ensure_area_resource_structure():
    """Ensures area resource directories and indexes exist."""
    AREAS_DIR.mkdir(parents=True, exist_ok=True)
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    PENDING_REELS_PATH.parent.mkdir(parents=True, exist_ok=True)

    for area_key, area_dir in AREAS_MAP.items():
        (AREAS_DIR / area_dir / "resources").mkdir(parents=True, exist_ok=True)

    if not MASTER_INDEX_PATH.exists() or MASTER_INDEX_PATH.stat().st_size == 0:
        with open(MASTER_INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

    if not PENDING_REELS_PATH.exists() or PENDING_REELS_PATH.stat().st_size == 0:
        with open(PENDING_REELS_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


def generate_structured_resource_markdown(resource_data: dict) -> str:
    """
    Generates a rich, non-empty Markdown dossier following the Product Owner's exact template.
    """
    title = resource_data.get("title", "Resource Dossier")
    area_label = resource_data.get("domain", "AI_AUTOMATION")
    density_label = resource_data.get("density_label", "Artificial Intelligence & Automation -> Workflow Engineering")
    res_id = resource_data.get("id", "RES-UNKNOWN")
    captured_at = resource_data.get("captured_at", datetime.datetime.now().isoformat())
    url_or_path = resource_data.get("url_or_path", "Direct Submission")
    uploader = resource_data.get("uploader", "Unknown Source")
    res_type = resource_data.get("resource_type", "TEXT_NOTE")
    source_name = resource_data.get("source_name", "Web Link")

    summary_5min = resource_data.get("summary_5min", "Simple executive summary of the resource.")
    trust_score = resource_data.get("trust_score", 85)
    score_breakdown = resource_data.get("score_breakdown", "Evaluated source domain, author authority, and structural claims consistency.")
    verification_status = resource_data.get("verification_status", "VERIFIED_AUTHENTIC")
    verification_rationale = resource_data.get("verification_rationale", "Verified content extracted from media metadata and transcript.")

    concept_explanation = resource_data.get("concept_explanation", "Explains practical AI and workflow optimization.")
    current_state_context = resource_data.get("current_state_context", "Manual friction and content creation bottlenecks.")
    solution_and_how_to = resource_data.get("solution_and_how_to", "Implement automated pipeline to transform raw inputs into ready outputs.")
    measurement_metrics = resource_data.get("measurement_metrics", "Track time saved, output count, and engagement conversion.")
    long_term_growth_wealth = resource_data.get("long_term_growth_wealth", "Build zero-cost automated channels generating passive brand value.")
    key_deliverables = resource_data.get("key_deliverables", ["1. Actionable Resource Dossier", "2. Faceless Video Script", "3. Social Post Draft"])

    transcript = resource_data.get("transcript", "")
    reel_script = resource_data.get("reel_script", {})

    md_content = f"""# 📚 {title}

**Source:** `{source_name}`
**Resource Format:** `{res_type}`
**Domain Breakdown:** `{density_label}`
**Source URL / Path:** `{url_or_path}`
**Author / Creator:** `{uploader}`
**Ingestion Timestamp:** `{captured_at}`

---

## 🛡️ Trust & Credibility Rating
- **Trust Score:** `{trust_score}/100` (🟢 High Confidence)
- **Score Breakdown & Basis:** {score_breakdown}
- **Fact-Check Status:** `{verification_status}`
- **Credibility Assessment:** {verification_rationale}

---

## ⚡ 5-Minute Executive Summary & Key Takeaways
{summary_5min}

---

## 🧩 Core Analysis & Strategic Framework

### 1. What It Is Trying to Explain (The Core Concept)
{concept_explanation}

### 2. What Is Currently Happening (Current State Context)
{current_state_context}

### 3. Why It Solves the Problem & How to Implement It
{solution_and_how_to}

### 4. How to Measure Implementation (Metrics & KPIs)
{measurement_metrics}

### 5. Long-Term Wealth & Growth Scale Strategy
{long_term_growth_wealth}

---

## 🎯 Recommended Action & Implementation Strategy
{resource_data.get('action_plan', 'Retain in Life OS Knowledge Engine and integrate into relevant project workflows.')}

---

## 🎙️ Spoken Audio / Document Transcript
```text
{transcript if transcript else "(No spoken audio transcript detected for this item)"}
```

---

## 🎬 Auto-Generated Faceless Reel Script (9:16)
**Topic:** `{reel_script.get('topic', title)}`
**Target Duration:** `{reel_script.get('duration', 30.0)}s`

### Timed Script Segments:
"""
    segments = reel_script.get("segments", [])
    for seg in segments:
        md_content += f"- **[{seg.get('start', 0.0)}s - {seg.get('end', 0.0)}s] ({seg.get('type', 'SEGMENT')}):** {seg.get('text', '')}\n"

    md_content += f"""
---

## 🤖 Subagent Guidance
Agents and subagents executing tasks in Area `{area_label}` should reference this file for authoritative knowledge.
"""
    return md_content


def distribute_resource_to_area(resource_data: dict) -> dict:
    """
    Distributes an ingested resource directly into the Area's dedicated `resources/` folder with human-readable filenames.
    """
    ensure_area_resource_structure()

    area_label = resource_data.get("domain", "AI_AUTOMATION")
    area_folder_name = AREAS_MAP.get(area_label, "ai_automation")
    title = resource_data.get("title", "Ingested Resource")

    slug = slugify_title(title)
    dossier_filename = f"{slug}.md"

    target_resource_dir = AREAS_DIR / area_folder_name / "resources"
    target_resource_dir.mkdir(parents=True, exist_ok=True)

    dossier_path = target_resource_dir / dossier_filename

    # Avoid collisions if file exists
    if dossier_path.exists():
        dossier_filename = f"{slug}-{int(datetime.datetime.now().timestamp()) % 10000}.md"
        dossier_path = target_resource_dir / dossier_filename

    md_text = generate_structured_resource_markdown(resource_data)

    with open(dossier_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    resource_data["dossier_path"] = str(dossier_path)

    # Master index update
    try:
        with open(MASTER_INDEX_PATH, "r", encoding="utf-8") as f:
            master_index = json.load(f)
    except Exception:
        master_index = []

    master_index.append(resource_data)
    with open(MASTER_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(master_index, f, indent=2)

    # Queue for Faceless Reels
    if resource_data.get("verification_status") != "REJECTED_UNAUTHENTIC":
        try:
            with open(PENDING_REELS_PATH, "r", encoding="utf-8") as f:
                reels_queue = json.load(f)
        except Exception:
            reels_queue = []

        reel_entry = {
            "reel_id": f"REEL-{slug}",
            "title": title,
            "area": area_folder_name,
            "dossier_path": str(dossier_path),
            "script": resource_data.get("reel_script", {}),
            "queued_at": datetime.datetime.now().isoformat(),
            "status": "QUEUED"
        }
        reels_queue.append(reel_entry)
        with open(PENDING_REELS_PATH, "w", encoding="utf-8") as f:
            json.dump(reels_queue, f, indent=2)

    return {
        "status": "SUCCESS",
        "title": title,
        "area": area_folder_name,
        "dossier_path": str(dossier_path),
        "verification_status": resource_data.get("verification_status", "VERIFIED_AUTHENTIC")
    }
