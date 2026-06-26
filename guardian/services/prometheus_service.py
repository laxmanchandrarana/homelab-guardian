import requests


class PrometheusService:

    def __init__(self):
        self.url = "http://localhost:9090"

    def targets(self):
        return requests.get(
            f"{self.url}/api/v1/targets"
        ).json()

    def alerts(self):
        return requests.get(
            f"{self.url}/api/v1/alerts"
        ).json()

    def rules(self):
        return requests.get(
            f"{self.url}/api/v1/rules"
        ).json()

    def query(self, expression):
        return requests.get(
            f"{self.url}/api/v1/query",
            params={"query": expression},
        ).json()
