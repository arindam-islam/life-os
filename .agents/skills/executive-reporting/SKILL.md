---
name: executive-reporting
description: Executive status reporting format for Product Owner updates, non-technical outcome summarization, and approval request formatting.
---

# Executive Status Reporting Skill

This skill formats communication for the Product Owner.

## Structure

```text
LIFE OS — <task>

Status: 🟢 / 🟡 / 🔴

What changed:
<1-3 short sentences>

Why it matters:
<one short sentence>

Running now:
<what is actually live>

Next:
<what the system is doing next>

Need from me:
Nothing (or explicit approval question)
```

## Guidelines

- Keep under 20 lines total.
- Highlight live vs prepared states honestly.
- Never dump raw log tracebacks, full code blocks, or Docker config dumps on the owner.
