RULES = {
    "container_down": "restart",
    "restart_failed": "rollback",
    "restore_failed": "rollback",
    "high_cpu": "restart",
    "high_memory": "restart",
    "disk_full": "cleanup",
}

class HealingRules:

    def match(self, incident):

        message = incident["message"].lower()
        severity = incident["severity"].upper()

        # Critical failures
        if "container is down" in message:
            return "restart"

        if "container stopped" in message:
            return "restart"

        if "container unhealthy" in message:
            return "restart"

        # Resource alerts
        if "high cpu" in message:
            return "notify"

        if "high memory" in message:
            return "notify"

        if "disk full" in message:
            return "cleanup"

        if "disk usage" in message:
            return "cleanup"

        # Escalation
        if severity == "CRITICAL":
            return "restart"

        return "ignore"
