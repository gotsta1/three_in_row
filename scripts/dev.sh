#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

if [ ! -f backend/.venv/bin/activate ]; then
  python3 -m venv backend/.venv
fi
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
export DATABASE_URL=${DATABASE_URL:-postgresql+asyncpg://postgres:postgres@localhost:5432/three_in_row}
uvicorn src.main:app --app-dir backend/src --reload
