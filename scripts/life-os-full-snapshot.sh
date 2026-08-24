#!/bin/bash

echo "====================================="
echo " LIFE OS COMPLETE SYSTEM SNAPSHOT"
echo " $(date)"
echo "====================================="

echo ""
echo "===== MACHINE ====="
hostname
pwd

echo ""
echo "===== GIT STATUS ====="
git branch --show-current
git status
echo ""
git log -5 --oneline

echo ""
echo "===== GIT REMOTE ====="
git remote -v

echo ""
echo "===== DOCKER STATUS ====="
docker compose ps

echo ""
echo "===== ACTIVE GOALS ====="
if [ -f ".life-os/goals/index.json" ]; then
python3 - <<'PY'
import json
with open(".life-os/goals/index.json") as f:
    goals=json.load(f)

for g in goals:
    print(
        g["goal_id"],
        "|",
        g["title"],
        "|",
        g["slug"]
    )
PY
fi

echo ""
echo "===== LIFE OS DIRECTORIES ====="
find .life-os -maxdepth 2 -type d | sort

echo ""
echo "===== PYTEST ====="
python3 -m pytest --collect-only -q

echo ""
echo "===== ENVIRONMENT ====="
python3 --version
docker --version

echo ""
echo "===== END SNAPSHOT ====="
