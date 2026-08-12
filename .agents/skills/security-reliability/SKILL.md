---
name: security-reliability
description: Security & Reliability Reviewer rules for secret handling, least privilege, zero-trust credential exposure, telemetry boundaries, network exposure, and production rollback safety.
---

# Security & Reliability Review Skill

This skill enforces security boundaries, data protection, and system reliability.

## Rules

1. **Zero Secret Leakage:** Never print, commit, or log `.env` secrets, tokens, credentials, or private captured content.
2. **Production SSH Security:** Always use `life-os-prod` SSH alias and key `~/.ssh/life-os-prod`. Never copy private key contents into prompts or repository files.
3. **Telemetry Boundary:** Expose operational metadata ONLY (health, execution counts, status, timestamps). Never allow payloads or personal data to cross into telemetry endpoints.
4. **Network Exposure & Least Privilege:** Keep services on internal Docker networks (`n8n_default`). Publish loopback-only ports (`127.0.0.1`).
5. **Rollback Verification:** Ensure pre-planned rollbacks are defined and narrower than or equal to the deployment scope before executing changes.
