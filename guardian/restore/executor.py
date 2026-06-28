from pathlib import Path
import subprocess

BACKUP_ROOT = Path("/mnt/storage/Backup/backups")
SERVICES_ROOT = Path("/home/sonjoy/server-services")


class RestoreExecutor:

    def execute(self, filename):

        backup = BACKUP_ROOT / filename

        if not backup.exists():
            raise FileNotFoundError(filename)

        compose_files = list(SERVICES_ROOT.rglob("docker-compose.yml"))

        stdout = ""
        stderr = ""

        for compose in compose_files:

            result = subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    str(compose),
                    "down",
                ],
                capture_output=True,
                text=True,
            )

            stdout += result.stdout
            stderr += result.stderr

        for compose in compose_files:

            result = subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    str(compose),
                    "up",
                    "-d",
                ],
                capture_output=True,
                text=True,
            )

            stdout += result.stdout
            stderr += result.stderr

        return {
            "returncode": 0,
            "stdout": stdout,
            "stderr": stderr,
        }
