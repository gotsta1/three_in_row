#!/usr/bin/env bash
set -e

alembic upgrade head
PORT="${PORT:-8000}"
exec uvicorn src.main:app --host 0.0.0.0 --port "${PORT}"
