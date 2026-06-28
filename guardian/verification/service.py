import socket
import time

from guardian.services.docker_service import DockerService


class VerificationService:

    def __init__(self):
        self.docker = DockerService()

    def verify(self, service):

        # Give container time to start
        time.sleep(10)

        container = self.docker.get(service)
        container.reload()

        if container.status != "running":
            return False, "Container is not running."

        state = container.attrs.get("State", {})

        health = state.get("Health")

        if health:
            if health.get("Status") != "healthy":
                return False, f"Health={health.get('Status')}"

        return True, "Healthy"
