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
