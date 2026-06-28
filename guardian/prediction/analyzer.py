class TrendAnalyzer:

    def analyze(self, history):

        if len(history) < 3:
            return {
                "risk": 0,
                "reason": "Insufficient history",
            }

        cpu = [x.get("cpu", 0) for x in history]
        memory = [x.get("memory", 0) for x in history]
        disk = [x.get("disk", 0) for x in history]

        risk = 0
        reasons = []

        # CPU continuously rising
        if cpu == sorted(cpu) and cpu[-1] > cpu[0]:
            risk += 30
            reasons.append("CPU increasing")

        # Memory continuously rising
        if memory == sorted(memory) and memory[-1] > memory[0]:
            risk += 30
            reasons.append("Memory increasing")

        # Disk usage continuously rising
        if disk == sorted(disk) and disk[-1] > disk[0]:
            risk += 40
            reasons.append("Disk usage increasing")

        return {
            "risk": min(risk, 100),
            "reason": ", ".join(reasons) if reasons else "Healthy",
        }
