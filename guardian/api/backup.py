from fastapi import APIRouter

from guardian.backup.service import BackupService

from guardian.repositories.backup_repo import BackupRepository

repo = BackupRepository()

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

@router.get("/history")
def history():

    backups = repo.list()

    return [
        {
            "id": b.id,
            "filename": b.filename,
            "size": b.size,
            "status": b.status,
            "created": b.created,
        }

        for b in backups
    ]


