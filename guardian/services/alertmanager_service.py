import requests


class AlertmanagerService:

    def __init__(self):
        self.url = "http://localhost:9093"

    def alerts(self):
        return requests.get(
            f"{self.url}/api/v2/alerts"
        ).json()

    def silences(self):
        return requests.get(
            f"{self.url}/api/v2/silences"
        ).json()
