# Ensure you are in your project root directory
cd ~/projects/homelab-guardian

# Step 1 — Create the Backup Structure
mkdir -p guardian/backup

touch guardian/backup/__init__.py
touch guardian/backup/history.py
touch guardian/backup/verify.py
touch guardian/backup/restore.py

# Step 2 — Create Backup Model
cat << 'EOF' > guardian/backup/models.py
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BackupJob:
    name: str
    backup_type: str
    destination: str
    created: datetime
    status: str
    size: int = 0
EOF

# Step 3 — Create Backup Engine
cat << 'EOF' > guardian/backup/engine.py
import subprocess
from pathlib import Path
from datetime import datetime


BACKUP_ROOT = Path("/mnt/storage/Backup/backups")


class BackupEngine:

    def create_directory(self):

        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

    def timestamp(self):

        return datetime.now().strftime("%Y%m%d-%H%M%S")

    def run(self, command):

        return subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )

    def docker_backup(self):

        self.create_directory()

        filename = BACKUP_ROOT / f"docker-{self.timestamp()}.tar.gz"

        cmd = f"tar czf {filename} /home/sonjoy/server-services"

        return self.run(cmd)
EOF

# Step 4 — Create Backup Service
cat << 'EOF' > guardian/backup/service.py
from guardian.backup.engine import BackupEngine


class BackupService:

    def __init__(self):
        self.engine = BackupEngine()

    def run(self):

        return self.engine.docker_backup()
EOF

# Step 5 — Create Backup API routes
cat << 'EOF' > guardian/api/backup.py
from fastapi import APIRouter

from guardian.backup.service import BackupService

router = APIRouter(
    prefix="/backup",
    tags=["Backup"],
)

service = BackupService()


@router.post("/run")
def run_backup():

    result = service.run()

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
EOF

# Step 6 — Re-compile app.py to include all routers gracefully
cat << 'EOF' > guardian/api/app.py
from fastapi import FastAPI

from guardian.api.routes import router
from guardian.api.monitoring import router as monitoring_router
from guardian.api.backup import router as backup_router

app = FastAPI(
    title="Homelab Guardian",
    description="Self Healing Homelab",
    version="0.1.0"
)

app.include_router(router)
app.include_router(monitoring_router)
app.include_router(backup_router)
EOF

# Step 7 — Restart and verify the systemd execution framework
sudo systemctl restart homelab-guardian

echo "--------------------------------------------------------"
echo "✅ Phase 3.3 Backup Engine API added and systemd reloaded!"
echo "📡 Test out the runner using: curl -X POST http://localhost:8008/backup/run"
echo "--------------------------------------------------------"
sudo systemctl status homelab-guardian --no-pager
