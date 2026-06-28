import subprocess


class RestoreHealth:

    def containers(self):
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--format",
                "{{.Names}}|{{.Status}}",
            ],
            capture_output=True,
            text=True,
        )

        containers = []

        for line in result.stdout.splitlines():
            if not line.strip():
                continue

            name, status = line.split("|", 1)

            containers.append(
                {
                    "name": name,
                    "status": status,
                }
            )

        return containers

    def check(self):

        containers = self.containers()

        unhealthy = []

        for c in containers:

            s = c["status"].lower()

            if (
                "unhealthy" in s
                or "restarting" in s
                or "exited" in s
                or "dead" in s
            ):
                unhealthy.append(c)

        return {
            "healthy": len(unhealthy) == 0,
            "total": len(containers),
            "failed": unhealthy,
            "containers": containers,
        }

