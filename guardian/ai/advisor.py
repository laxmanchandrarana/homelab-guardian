class RecoveryAdvisor:

    ACTIONS = {
        "OUT_OF_MEMORY": (
            "restart",
            "Container likely ran out of memory.",
        ),

        "DISK_FULL": (
            "cleanup_disk",
            "Disk is full.",
        ),

        "PERMISSION": (
            "fix_permissions",
            "Permission issue detected.",
        ),

        "DATABASE_DOWN": (
            "restart_database",
            "Database appears unavailable.",
        ),

        "NETWORK": (
            "restart_network",
            "Network connectivity problem.",
        ),

        "HEALTHCHECK": (
            "restart",
            "Container healthcheck failed.",
        ),

        "CRASH": (
            "rollback",
            "Application crash detected.",
        ),

        "DEPENDENCY": (
            "notify",
            "Missing dependency requires manual intervention.",
        ),

        "MANUAL_STOP": (
            "ignore",
            "Container was intentionally stopped.",
        ),

        "UNKNOWN": (
            "restart",
            "Unknown failure, attempt restart.",
        ),
    }

    def recommend(self, analysis):

        cause = analysis["cause"]

        action, reason = self.ACTIONS.get(
            cause,
            self.ACTIONS["UNKNOWN"],
        )

        return {
            "action": action,
            "reason": reason,
        }
