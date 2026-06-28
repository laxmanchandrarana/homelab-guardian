from pathlib import Path
from fastapi import APIRouter, HTTPException
from guardian.restore.verify import VerifyEngine
from guardian.restore.planner import RestorePlanner
from guardian.restore.service import RestoreService
from guardian.restore.jobs import RestoreJobs
from guardian.repositories.restore_repo import RestoreRepository
from guardian.restore.health import RestoreHealth
from guardian.restore.rollback import RollbackService

rollback_service = RollbackService()
health = RestoreHealth()
restore_repo = RestoreRepository()
planner = RestorePlanner()
verify = VerifyEngine()
restore_service = RestoreService()
restore_jobs = RestoreJobs()

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

@router.post("/run/{filename}")
def run_restore(filename: str):
    return restore_service.run(filename)

@router.get("/job/{filename}")
def restore_job(filename: str):
    job = restore_jobs.get(filename)

    if not job:
        return {
            "exists": False
        }

    return job

@router.get("/history")
def restore_history():
    rows = restore_repo.list()

    return [
        {
            "id": r.id,
            "filename": r.filename,
            "started": r.started,
            "completed": r.completed,
            "status": r.status,
        }
        for r in rows
    ]


@router.get("/health")
def restore_health():
    return health.check()

@router.post("/rollback/{filename}")
def rollback(filename: str):
    return rollback_service.rollback(filename)


