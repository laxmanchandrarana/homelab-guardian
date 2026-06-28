from guardian.diagnostics.rules import DiagnosisRules


class DiagnosisEngine:

    def diagnose(self, logs: str):

        text = logs.lower()

        for rule in DiagnosisRules.RULES:

            if rule["pattern"] in text:

                return {
                    "cause": rule["cause"],
                    "confidence": rule["confidence"],
                }

        return {
            "cause": "UNKNOWN",
            "confidence": 0.50,
        }
