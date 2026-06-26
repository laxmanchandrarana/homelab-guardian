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
