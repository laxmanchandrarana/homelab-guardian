import time

from guardian.monitoring.scanner import DockerScanner
from guardian.monitoring.detector import IncidentDetector
from guardian.healing.service import HealingService
from guardian.notifications.service import NotificationService
from guardian.prediction import prediction_service


class GuardianDaemon:

    def __init__(self):

        self.scanner = DockerScanner()
        self.detector = IncidentDetector()
        self.healer = HealingService()
        self.notifications = NotificationService()

    def run(self):

        while True:

            containers = self.scanner.scan()

            print("Guardian scan...", len(containers))

            for container in containers:

                service = container["name"]

                prediction = prediction_service.predict(service)

                risk = prediction["prediction"]["risk"]

                if risk >= 90:

                    self.notifications.send(
                        title="Critical Failure Prediction",
                        message=(
                            f"{service} has a predicted failure risk of "
                            f"{risk}%.\n"
                            f"{prediction['prediction']['reason']}"
                        ),
                    )

                elif risk >= 70:

                    self.notifications.send(
                        title="High Risk Warning",
                        message=(
                            f"{service} has a predicted failure risk of "
                            f"{risk}%.\n"
                            f"{prediction['prediction']['reason']}"
                        ),
                    )

            incidents = self.detector.detect(containers)

            for incident in incidents:

                self.healer.heal(
                    severity=incident["severity"],
                    service=incident["service"],
                    message=incident["message"],
                )

            time.sleep(30)
