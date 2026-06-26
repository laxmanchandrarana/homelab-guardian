#!/bin/bash

cd ~/projects/homelab-guardian

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

exec uvicorn guardian.api.app:app \
--host 0.0.0.0 \
--port 8008
