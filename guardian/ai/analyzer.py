from guardian.diagnostics.service import DiagnosisService


class FailureAnalyzer:

    def __init__(self):
        self.diagnosis = DiagnosisService()

    def analyze(self, data):

        result = self.diagnosis.diagnose(
            data["logs"]
        )

        return result
