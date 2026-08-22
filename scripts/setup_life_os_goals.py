#!/usr/bin/env python3
"""
Life OS — Machine-Readable Goals Architecture Setup
Creates `.life-os/goals/` directory, initializes `index.json`, and generates structured Markdown goal dossiers.
"""

import os
import json
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
LIFE_OS_DIR = BASE_DIR / ".life-os"
GOALS_DIR = LIFE_OS_DIR / "goals"
GOALS_INDEX_PATH = GOALS_DIR / "index.json"

MASTER_GOALS = [
    {
        "goal_id": "GOAL-001",
        "title": "₹15 Lakhs Net Revenue Target by Dec 31, 2026",
        "category": "CAREER_WEALTH",
        "status": "ACTIVE",
        "target_date": "2026-12-31",
        "budget_cap": "$0 Host Cost (Oracle Cloud Free Tier)",
        "description": "Monetize B2B automation services, digital AI tools, and content engine to generate ₹15 Lakhs net revenue.",
        "kpis": ["₹15,00,000 Total Net Revenue", "$0 Infrastructure Host Expenses", "3 Paid B2B Retainers ($1,500/mo)"],
        "slug": "goal-001-revenue-15L-dec-2026"
    },
    {
        "goal_id": "GOAL-002",
        "title": "Autonomous Faceless AI Video & Shorts Engine",
        "category": "CREATIVE_CONVERSATIONS",
        "status": "ACTIVE",
        "target_date": "2026-09-30",
        "budget_cap": "$0 Host Cost",
        "description": "Build an end-to-end automated script-to-video pipeline rendering 9:16 vertical reels and shorts for YouTube and Instagram.",
        "kpis": ["1 Daily Automated Reel Rendered", "Zero Manual Editing Required", "10,000+ Total Views Across Channels"],
        "slug": "goal-002-faceless-ai-content-engine"
    },
    {
        "goal_id": "GOAL-003",
        "title": "24/7 Mobile Slack Command Center & Thread Workforce",
        "category": "AI_AUTOMATION",
        "status": "ACTIVE",
        "target_date": "2026-08-31",
        "budget_cap": "$0 Host Cost",
        "description": "Deploy autonomous Slack workforce agents on Oracle VM. Enable conversational execution via thread replies ('Alright let's do it').",
        "kpis": ["24/7 Up-Time on Oracle VM", "<10s Thread Reaction Time", "Zero MacBook Dependency for Remote Commands"],
        "slug": "goal-003-mobile-slack-command-center"
    },
    {
        "goal_id": "GOAL-004",
        "title": "Multimodal Ingestion Pipeline & Verification Wall",
        "category": "PRODUCTIVITY_HACKS",
        "status": "ACTIVE",
        "target_date": "2026-08-31",
        "budget_cap": "$0 Host Cost",
        "description": "Ingest YouTube, LinkedIn, Instagram, PDFs, and spoken audio into clean area resource dossiers passing the Authenticity Wall.",
        "kpis": ["100% Ingested Resources Categorized", "0 Fake/Bait Content Admitted", "Human-Readable Dossier Paths Generated"],
        "slug": "goal-004-multimodal-ingestion-verification-wall"
    }
]


def setup_goals():
    GOALS_DIR.mkdir(parents=True, exist_ok=True)

    goal_index = []
    for g in MASTER_GOALS:
        goal_file = GOALS_DIR / f"{g['slug']}.md"
        md_content = f"""# 🎯 {g['goal_id']}: {g['title']}

**Goal ID:** `{g['goal_id']}`
**Category / Area:** `{g['category']}`
**Status:** `{g['status']}`
**Target Completion Date:** `{g['target_date']}`
**Budget Boundary:** `{g['budget_cap']}`

---

## 📝 Objective & Description
{g['description']}

---

## 📊 Key Performance Indicators (KPIs)
"""
        for kpi in g['kpis']:
            md_content += f"- ✅ {kpi}\n"

        md_content += f"""
---

## 📂 Connected Resource Dossiers & Slack Discussions
*Thread discussions on Slack (#life-os-resource-inbox) replying to resource summaries will automatically link here.*

---

## 🤖 Agent Execution Strategy
Subagents operating under Area `{g['category']}` should prioritize action items that directly advance this goal's KPIs.
"""
        with open(goal_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        g["file_path"] = str(goal_file)
        goal_index.append(g)

    with open(GOALS_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(goal_index, f, indent=2)

    print(f"✅ Initialized Life OS Goals Architecture: {len(goal_index)} Master Goals created in {GOALS_DIR}")


if __name__ == "__main__":
    setup_goals()
