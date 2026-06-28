from guardian.alerts.parser import AlertParser
from guardian.healing.service import HealingService


class AlertService:

    def __init__(self):
        self.parser = AlertParser()
        self.healer = HealingService()

    def process(self, payload):

        incidents = self.parser.parse(payload)

        results = []

        for incident in incidents:

            result = self.healer.heal(
                severity=incident["severity"],
                service=incident["service"],
                message=incident["message"],
            )

            results.append({
                "incident": incident,
                "result": result,
            })

        return results
