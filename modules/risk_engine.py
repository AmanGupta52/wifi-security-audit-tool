class RiskEngine:
    def calculate(self, encryption, protection, password):
        score = encryption["score"]

        if not protection["pmf_enabled"]:
            score += 2
        if protection["wps_enabled"]:
            score += 2
        if password["strength"] == "Weak":
            score += 3

        if score >= 10:
            level = "Critical"
        elif score >= 7:
            level = "High"
        elif score >= 4:
            level = "Medium"
        else:
            level = "Low"

        return {
            "score": score,
            "level": level
        }
