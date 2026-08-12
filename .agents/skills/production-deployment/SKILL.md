---
name: production-deployment
description: Production deployment discipline and safety invariants for Life OS production updates on Oracle host via life-os-prod.
---

# Production Deployment Skill

This skill governs deployment safety and production container operations.

## Protocol Sequence

1. **Local Pre-flight:** Verify clean working tree (`git diff --check`) and passing unit tests.
2. **Git Push:** Push committed changes to GitHub `main` branch.
3. **Identity Snapshot:** SSH to `life-os-prod` and record container IDs and status (`docker ps`).
4. **Targeted Service Pull & Up:** Target only named service:
   ```sh
   ssh life-os-prod "cd /home/ubuntu/projects/n8n && git pull origin main && docker compose build <service> && docker compose up -d --no-deps <service>"
   ```
5. **Post-flight Verification:** Re-check container health endpoints and confirm untouched containers retained their original IDs.
6. **Narrow Rollback:** If post-deployment checks fail, execute narrow service rollback immediately.
