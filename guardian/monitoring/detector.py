from guardian.monitoring.state_cache import state_cache


class IncidentDetector:

    def detect(self, containers):
        incidents = []

        for container in containers:
            name = container["name"]
            status = container.get("status", "").lower()

            if not state_cache.changed(name, status):
                continue

            if "unhealthy" in status:
                incidents.append({
                    "severity": "CRITICAL",
                    "service": name,
                    "message": "Container unhealthy",
                })

            elif "exited" in status:
                incidents.append({
                    "severity": "CRITICAL",
                    "service": name,
                    "message": "Container stopped",
                })

        return incidents
