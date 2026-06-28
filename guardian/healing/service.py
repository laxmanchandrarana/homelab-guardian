from datetime import datetime

from guardian.healing.engine import HealingEngine
from guardian.repositories.incident_repo import IncidentRepository
from guardian.models.incident import Incident


class HealingService:

    def __init__(self):
        self.engine = HealingEngine()
        self.repo = IncidentRepository()

    def heal(self, severity, service, message):

        result = self.engine.heal(
            {
                "severity": severity,
                "service": service,
                "message": message,
            }
        )

        incident = Incident(
            created=datetime.now(),
            severity=severity,
            service=service,
            message=message,
            healed="YES" if result.get("success") else "FAILED",
        )

        self.repo.add(incident)

        return result
