from pathlib import Path

from fastapi import APIRouter, HTTPException

from guardian.restore.verify import VerifyEngine

from guardian.restore.planner import RestorePlanner

planner = RestorePlanner()

verify = VerifyEngine()

router = APIRouter(
    prefix="/restore",
    tags=["Restore"]
)

BACKUP_DIR = Path("/mnt/storage/Backup/backups")

@router.get("/backups")
def list_backups():
    if not BACKUP_DIR.exists():
        return []

    backups = []

    for backup in sorted(BACKUP_DIR.glob("*.tar.gz"), reverse=True):
        stat = backup.stat()

        backups.append({
            "name": backup.name,
            "size": stat.st_size,
            "modified": stat.st_mtime
        })

    return backups


@router.get("/backup/{name}")
def backup_info(name: str):

    file = BACKUP_DIR / name

    if not file.exists():
        raise HTTPException(404, "Backup not found")

    stat = file.stat()

    return {
        "name": file.name,
        "size": stat.st_size,
        "modified": stat.st_mtime
    }

@router.get("/verify/{name}")
def verify_backup(name: str):

    file = BACKUP_DIR / name

    return verify.verify(file)

@router.get("/plan/{name}")
def restore_plan(name: str):

    backup = BACKUP_DIR / name

    return planner.analyze(backup)


