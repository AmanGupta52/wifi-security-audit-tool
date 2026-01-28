class EncryptionAnalyzer:
    def analyze(self, network):
        enc = network["encryption"]

        score_map = {
            "OPEN": ("Critical", 9),
            "WEP": ("Critical", 9),
            "WPA": ("High", 7),
            "WPA2": ("Medium", 5),
            "WPA3": ("Low", 2)
        }

        severity, score = score_map.get(enc, ("Unknown", 5))

        return {
            "type": enc,
            "severity": severity,
            "score": score
        }
