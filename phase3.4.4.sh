# Ensure you are in your project root directory
cd ~/projects/homelab-guardian

# Step 1 — Create metadata helper
cat << 'EOF' > guardian/backup/metadata.py
from pathlib import Path
from datetime import datetime
import hashlib


class BackupMetadata:

    def filename(self, path: Path):
        return path.name

    def filesize(self, path: Path):
        return path.stat().st_size

    def created(self, path: Path):
        return datetime.fromtimestamp(path.stat().st_ctime)

    def sha256(self, path: Path):
        h = hashlib.sha256()

        with open(path, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()
EOF

# Step 2 — Modify BackupEngine (Includes BackupMetadata integration)
cat << 'EOF' > guardian/backup/engine.py
import subprocess
from pathlib import Path
from datetime import datetime
from guardian.backup.metadata import BackupMetadata

BACKUP_ROOT = Path("/mnt/storage/Backup/backups")
metadata = BackupMetadata()


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

        cmd = (
            f"sudo /usr/bin/tar "
            f"--warning=no-file-changed "
            f"--ignore-failed-read "
            f"-czpf {filename} "
            f"/home/sonjoy/server-services"
        )

        result = self.run(cmd)

        data = {
            "process": result,
            "path": filename,
        }

        if filename.exists():
            data["filename"] = metadata.filename(filename)
            data["size"] = metadata.filesize(filename)
            data["created"] = metadata.created(filename)
            data["sha256"] = metadata.sha256(filename)

        return data
EOF

# Step 3 — Update BackupService
cat << 'EOF' > guardian/backup/service.py
from guardian.backup.engine import BackupEngine
from guardian.repositories.backup_repo import BackupRepository
from guardian.models.backup import Backup
from guardian.repositories.audit_repo import AuditRepository
from guardian.models.audit import Audit


class BackupService:

    def __init__(self):
        self.engine = BackupEngine()
        self.repo = BackupRepository()
        self.audit = AuditRepository()

    def run(self):
        result = self.engine.docker_backup()
        process = result["process"]

        if "filename" in result:
            status = "SUCCESS" if process.returncode == 0 else "FAILED"

            backup = Backup(
                filename=result["filename"],
                sha256=result["sha256"],
                size=result["size"],
                created=result["created"],
                verified=False,
                location=str(result["path"]),
                status=status,
            )
            self.repo.add(backup)

            audit = Audit(
                action=f"BACKUP_{status}",
                resource=result["filename"],
                status=status,
            )
            self.audit.add(audit)

        return process
EOF

# Step 4 — Verify and Update Audit Repository
mkdir -p guardian/repositories
cat << 'EOF' > guardian/repositories/audit_repo.py
from guardian.database import SessionLocal
from guardian.models.audit import Audit


class AuditRepository:

    def add(self, audit):
        db = SessionLocal()
        db.add(audit)
        db.commit()
        db.refresh(audit)
        db.close()
        return audit

    def list(self):
        db = SessionLocal()
        rows = db.query(Audit).order_by(Audit.id.desc()).all()
        db.close()
        return rows
EOF

# Step 5 & 6 — Improve History API & Add Latest Endpoint
cat << 'EOF' > guardian/api/backup.py
from fastapi import APIRouter
from guardian.backup.service import BackupService
from guardian.repositories.backup_repo import BackupRepository

router = APIRouter(
    prefix="/backup",
    tags=["Backup"],
)

service = BackupService()
repo = BackupRepository()


@router.post("/run")
def run_backup():
    result = service.run()
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


@router.get("/history")
def history():
    backups = repo.list()
    return [
        {
            "id": b.id,
            "filename": b.filename,
            "size": f"{round(b.size / (1024**3), 2)} GB" if b.size else None,
            "sha256": b.sha256,
            "created": b.created,
            "verified": b.verified,
            "status": b.status,
        }
        for b in backups
    ]


@router.get("/latest")
def latest():
    b = repo.latest()
    if not b:
        return {}
    return {
        "id": b.id,
        "filename": b.filename,
        "size": b.size,
        "sha256": b.sha256,
        "created": b.created,
        "verified": b.verified,
        "status": b.status,
    }
EOF

# Step 7 — Restart API
sudo systemctl daemon-reload
sudo systemctl restart homelab-guardian

echo "--------------------------------------------------------"
echo "✅ Phase 3.4.4 Metadata Tracking added successfully!"
echo "📡 Test endpoints:"
echo "   - Run:    curl -X POST http://localhost:8008/backup/run"
echo "   - History: curl http://localhost:8008/backup/history"
echo "   - Latest:  curl http://localhost:8008/backup/latest"
echo "--------------------------------------------------------"
sudo systemctl status homelab-guardian --no-pager
