#!/usr/bin/env bash
# Seeds the MongoDB used by docker compose (same DB as the api service)
# Requires: docker compose stack up (at least mongo)
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose run --rm api python /app/src/app/utils/init/create_init_state.py
