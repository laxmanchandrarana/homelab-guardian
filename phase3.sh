# Ensure you are in your project root directory
cd ~/projects/homelab-guardian

# Step 1 — Install FastAPI inside the virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    pip install fastapi uvicorn pydantic python-multipart
    pip freeze > requirements.txt
else
    echo "⚠️ .venv not found! Installing globally/system-wide context or current environment."
    pip install fastapi uvicorn pydantic python-multipart
fi

# Step 2 — Create API Structure
mkdir -p guardian/api bin

# Step 3 — Create the FastAPI Application
cat << 'EOF' > guardian/api/app.py
from fastapi import FastAPI

from guardian.api.routes import router

app = FastAPI(
    title="Homelab Guardian",
    description="Self Healing Homelab",
    version="0.1.0"
)

app.include_router(router)
EOF

# Step 4 — Create API Routes (Adjusted to match Phase 2.3 list() method)
cat << 'EOF' > guardian/api/routes.py
from fastapi import APIRouter

from guardian.services.docker_service import DockerService
from guardian.core.health import Health

router = APIRouter()

docker = DockerService()
health = Health()


@router.get("/")
def root():
    return {
        "project": "Homelab Guardian",
        "status": "running"
    }


@router.get("/health")
def health_api():
    return {
        "cpu": health.cpu(),
        "memory": health.memory(),
        "disk": health.disk()
    }


@router.get("/containers")
def containers():
    result = []

    # Adjusted to .list() to match DockerService layout from Phase 2.3
    for c in docker.list():
        result.append({
            "name": c.name,
            "status": c.status,
            "image": c.image.tags
        })

    return result


@router.post("/restart/{container}")
def restart(container: str):

    docker.restart(container)

    return {
        "status": "restarted",
        "container": container
    }


@router.get("/logs/{container}")
def logs(container: str):

    return {
        "logs": docker.logs(container)
    }
EOF

# Step 7 — Add API Entry Point
cat << 'EOF' > api.py
from guardian.api.app import app
EOF

# Step 8 — Create Startup Script
cat << 'EOF' > bin/start-api.sh
#!/bin/bash

cd ~/projects/homelab-guardian

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

exec uvicorn guardian.api.app:app \
--host 0.0.0.0 \
--port 8008
EOF

chmod +x bin/start-api.sh

# Step 9 — Create and Enable Systemd Service
sudo tee /etc/systemd/system/homelab-guardian.service > /dev/null << 'EOF'
[Unit]
Description=Homelab Guardian API
After=network.target docker.service

[Service]
Type=simple
User=sonjoy
WorkingDirectory=/home/sonjoy/projects/homelab-guardian
ExecStart=/home/sonjoy/projects/homelab-guardian/.venv/bin/uvicorn guardian.api.app:app --host 0.0.0.0 --port 8008
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable homelab-guardian
sudo systemctl restart homelab-guardian

echo "--------------------------------------------------------"
echo "✅ Phase 3 REST API successfully configured and deployed!"
echo "📡 Interactive docs available at: http://YOUR_SERVER_IP:8008/docs"
echo "--------------------------------------------------------"
sudo systemctl status homelab-guardian --no-pager
