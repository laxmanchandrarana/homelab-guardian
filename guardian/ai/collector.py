from guardian.services.docker_service import DockerService


class LogCollector:

    def __init__(self):
        self.docker = DockerService()

    def collect(self, service):

        container = self.docker.get(service)

        try:
            health = (
                container.attrs["State"]
                .get("Health", {})
                .get("Status", "unknown")
            )
        except Exception:
            health = "unknown"

        try:
            restart_count = container.attrs["RestartCount"]
        except Exception:
            restart_count = 0

        try:
            exit_code = container.attrs["State"]["ExitCode"]
        except Exception:
            exit_code = None

        try:
            logs = self.docker.logs(service, tail=500)
        except Exception:
            logs = ""

        return {
            "service": service,
            "status": container.status,
            "health": health,
            "restart_count": restart_count,
            "exit_code": exit_code,
            "logs": logs,
            "inspect": container.attrs,
        }
