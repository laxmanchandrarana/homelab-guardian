from guardian.services.docker_service import DockerService


class RootCauseAnalyzer:

    def __init__(self):
        self.docker = DockerService()

    def analyze(self, service):

        try:
            container = self.docker.get(service)
            state = container.attrs["State"]

            status = state.get("Status", "")

            # Current state first
            if status == "running":
                return "Container is running normally."

            if status == "paused":
                return "Container is paused."

            if status == "restarting":
                return "Container is restarting."

            if status == "exited":

                if state.get("OOMKilled"):
                    return "Container exited because it was killed by OOM."

                exit_code = state.get("ExitCode", -1)

                if exit_code == 0:
                    return "Container was stopped gracefully."

                if exit_code == 1:
                    return "Application exited with an error."

                if exit_code == 137:
                    return "Container was killed (SIGKILL/OOM)."

                if exit_code == 143:
                    return "Container received SIGTERM."

                return f"Container exited with code {exit_code}."

            error = state.get("Error")
            if error:
                return error

            health = state.get("Health")
            if health:
                return f"Health status: {health.get('Status')}"

            return f"Status: {status}"

        except Exception as e:
            return str(e)
