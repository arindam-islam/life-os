---
name: staying-ahead-curator
description: AI Intelligence & Staying Ahead Curator process for inspecting https://stayingahead.com/daily-ai-updates via browser subagent, evaluating 14-step resource pipeline, and maintaining provenance deduplication state.
---

# Staying Ahead Curator Skill

This skill governs the evaluation of external AI intelligence from `https://stayingahead.com/daily-ai-updates`.

## 14-Step Evaluation Pipeline

1. **Deduplication Check:** Read `.life-os/sources/staying_ahead_processed.json` to verify if URL/resource has already been evaluated.
2. **Resource Capture:** Extract title, URL, date, author, resource type via browser/research tools.
3. **Principle Extraction:** Extract the actual idea, method, tool, prompt, or framework.
4. **Outcome Explanation:** Define what target outcome it improves for Life OS.
5. **Prerequisite Identification:** List required infrastructure, models, or accounts.
6. **Risk & Cost Assessment:** Identify financial cost, security risk, complexity, or vendor lock-in.
7. **Factual Verification:** Cross-reference tool claims against official docs or primary sources.
8. **Life OS Relevance:** Determine alignment with Life OS North Star and current active priorities.
9. **Decision Assignment:** Assign one of: `REJECT`, `ARCHIVE`, `KNOWLEDGE_ONLY`, `EXPERIMENT`, `ADOPT`, or `REPLACE_EXISTING_METHOD`.
10. **System Update Plan (if ADOPT):** Specify exact rule, skill, workflow, agent, or configuration to update.
11. **Safety Boundary Guard:** Governance and safety rules always override external recommendations.
12. **Provenance Logging:** Record full record in `.life-os/sources/staying_ahead_processed.json`.
13. **Changelog Update:** Log change in `.life-os/changelog/history.json`.
14. **Executive Reporting:** Summarize adopted items in founder status update under "What changed".
