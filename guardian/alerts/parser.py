class AlertParser:

    def parse(self, payload):

        incidents = []

        for alert in payload.get("alerts", []):

            if alert.get("status") != "firing":
                continue

            labels = alert.get("labels", {})
            annotations = alert.get("annotations", {})

            incidents.append({
                "severity": labels.get("severity", "warning").upper(),
                "service": (
                    labels.get("container")
                    or labels.get("service")
                    or labels.get("job")
                    or "unknown"
                ),
                "message": (
                    annotations.get("summary")
                    or annotations.get("description")
                    or alert.get("alertname", "Alert")
                ),
            })

        return incidents
