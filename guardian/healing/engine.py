import asyncio

from guardian.healing.rules import HealingRules
from guardian.restore.rollback import RollbackService
from guardian.services.docker_service import DockerService
from guardian.health.service import HealthService
from guardian.health.policy import HealthPolicy
from guardian.notifications.service import NotificationService
from guardian.analysis.root_cause import RootCauseAnalyzer
from guardian.verification.service import VerificationService
from guardian.api.events import publish


class HealingEngine:

    def __init__(self):
        self.rules = HealingRules()
        self.docker = DockerService()
        self.rollback = RollbackService()
        self.health = HealthService()
        self.policy = HealthPolicy()
        self.notifications = NotificationService()
        self.analyzer = RootCauseAnalyzer()
        self.verifier = VerificationService()

    def _broadcast(self, payload: dict):
        """
        Send realtime updates to dashboard clients.
        Works from FastAPI, daemon threads and CLI.
        """

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(
                publish("healing", payload)
            )
        except RuntimeError:
            asyncio.run(
                publish("healing", payload)
            )

    def heal(self, incident):

        service = incident["service"]

        self._broadcast({
            "stage": "received",
            "service": service,
            "incident": incident,
        })

        # ---------------------------------------------------------
        # Auto-healing disabled
        # ---------------------------------------------------------
        if not self.policy.is_enabled(service):

            self.notifications.send(
                title="Healing Ignored",
                message=f"{service} has auto-healing disabled."
            )

            self._broadcast({
                "stage": "ignored",
                "service": service,
                "reason": "Auto-healing disabled",
            })

            return {
                "success": False,
                "action": "ignored",
                "reason": "Auto-healing disabled",
            }

        # ---------------------------------------------------------
        # Match healing rule
        # ---------------------------------------------------------
        action = self.rules.match(incident)

        self._broadcast({
            "stage": "rule_matched",
            "service": service,
            "action": action,
        })

        # ---------------------------------------------------------
        # Ignore
        # ---------------------------------------------------------
        if action == "ignore":

            self._broadcast({
                "stage": "completed",
                "service": service,
                "action": "ignored",
            })

            return {
                "success": True,
                "action": "ignored",
            }

        # ---------------------------------------------------------
        # Notify only
        # ---------------------------------------------------------
        if action == "notify":

            self.notifications.send(
                title="Guardian Notification",
                message=f"{service}: {incident['message']}"
            )

            self._broadcast({
                "stage": "notify",
                "service": service,
            })

            return {
                "success": True,
                "action": "notify",
                "service": service,
                "message": incident["message"],
            }

        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if action == "cleanup":

            self.notifications.send(
                title="Cleanup Triggered",
                message=f"{service}: cleanup requested."
            )

            self._broadcast({
                "stage": "cleanup",
                "service": service,
            })

            return {
                "success": True,
                "action": "cleanup",
                "service": service,
            }

        # ---------------------------------------------------------
        # Unknown
        # ---------------------------------------------------------
        if action != "restart":

            self._broadcast({
                "stage": "unknown_action",
                "service": service,
                "action": action,
            })

            return {
                "success": False,
                "action": "unknown",
            }

        # ---------------------------------------------------------
        # Restart limit
        # ---------------------------------------------------------
        if not self.health.can_restart(service):

            self.notifications.send(
                title="Restart Blocked",
                message=f"{service} exceeded restart limit."
            )

            self._broadcast({
                "stage": "blocked",
                "service": service,
                "reason": "Restart limit reached",
            })

            return {
                "success": False,
                "action": "blocked",
                "reason": "Restart limit reached",
            }

        try:

            # -----------------------------------------------------
            # Root Cause Analysis
            # -----------------------------------------------------
            try:
                root_cause = self.analyzer.analyze(service)
            except Exception:
                root_cause = "Unknown"

            self._broadcast({
                "stage": "analysis",
                "service": service,
                "root_cause": root_cause,
            })

            # -----------------------------------------------------
            # Restart
            # -----------------------------------------------------
            self.docker.restart(service)

            self.health.restarted(service)

            self._broadcast({
                "stage": "restart",
                "service": service,
            })

            # -----------------------------------------------------
            # Verification
            # -----------------------------------------------------
            success, reason = self.verifier.verify(service)

            self._broadcast({
                "stage": "verification",
                "service": service,
                "success": success,
                "reason": reason,
            })

            # -----------------------------------------------------
            # Verification Failed
            # -----------------------------------------------------
            if not success:

                rollback = self.rollback.rollback(service)

                self.notifications.send(
                    title="Rollback Executed",
                    message=(
                        f"{service}\n\n"
                        f"Verification Failed\n"
                        f"{reason}"
                    )
                )

                self._broadcast({
                    "stage": "rollback",
                    "service": service,
                    "reason": reason,
                })

                return {
                    "success": False,
                    "action": "rollback",
                    "reason": reason,
                    "rollback": rollback,
                }

            # -----------------------------------------------------
            # Success
            # -----------------------------------------------------
            self.health.healed(service)

            self.notifications.send(
                title="Container Restarted",
                message=f"{service} restarted successfully."
            )

            self._broadcast({
                "stage": "completed",
                "service": service,
                "action": "restart",
                "success": True,
            })

            return {
                "success": True,
                "action": "restart",
                "service": service,
            }

        except Exception as exc:

            rollback = self.rollback.rollback(service)

            self.notifications.send(
                title="Rollback Executed",
                message=f"{service} failed with exception.\n\nRollback started."
            )

            self._broadcast({
                "stage": "exception",
                "service": service,
                "error": str(exc),
            })

            return {
                "success": False,
                "action": "rollback",
                "error": str(exc),
                "rollback": rollback,
            }
