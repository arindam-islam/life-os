# Life OS Architecture Decisions


## Decision 1

GitHub is the source of truth.

Reason:

Provides version control, rollback, and portability.


---


## Decision 2

OCI is production runtime.

Reason:

Always-on execution without depending on MacBook.


---


## Decision 3

Docker Compose remains deployment method.

Reason:

Simple, reproducible, maintainable.


---


## Decision 4

n8n is the automation orchestration layer.

Reason:

Supports workflows, integrations, and automation.


---


## Decision 5

AI models remain replaceable.

Reason:

Avoid vendor lock-in.

Life OS should work with Gemini, OpenAI, or other models.


---


## Decision 6

Telegram replaces Slack as personal command interface.

Reason:

Lower cost and better personal usability.
