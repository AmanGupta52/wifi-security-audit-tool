import yaml
import re

class PasswordAudit:
    def __init__(self):
        try:
            with open("./config.yaml", "r") as f:
                self.config = yaml.safe_load(f)
        except:
            self.config = {}

    def run(self, network):
        score = 0
        reasons = []

        encryption = network.get("encryption", "WPA2")
        ssid = network.get("ssid", "").lower()
        vendor = network.get("vendor", "Unknown")
        signal = abs(network.get("signal", -60))  # dBm positive value
        wps_enabled = network.get("wps", False) or network.get("wps_enabled", False)

        # ---------------------------
        # 1. Encryption scoring
        # ---------------------------
        if encryption == "WEP":
            score += 40
            reasons.append("WEP encryption is broken")
        elif encryption == "WPA":
            score += 25
            reasons.append("WPA is outdated")
        elif encryption == "WPA2":
            score += 10
        elif encryption == "WPA3":
            score += 2

        # ---------------------------
        # 2. WPS scoring
        # ---------------------------
        if wps_enabled:
            score += 25
            reasons.append("WPS enabled (PIN attack risk)")

        # ---------------------------
        # 3. SSID pattern scoring
        # ---------------------------
        weak_patterns = ["admin", "guest", "wifi", "home", "test", "default", "tplink", "dlink"]

        for p in weak_patterns:
            if p in ssid:
                score += 10
                reasons.append(f"Weak SSID pattern detected: {p}")
                break

        # ---------------------------
        # 4. Vendor scoring
        # ---------------------------
        weak_vendors = ["TP-Link", "D-Link", "Tenda", "Netgear"]

        if vendor in weak_vendors:
            score += 10
            reasons.append(f"Consumer router vendor: {vendor}")

        # ---------------------------
        # 5. Signal strength scoring
        # ---------------------------
        if signal < 50:
            score += 15
            reasons.append("Very strong signal (easy to attack nearby)")
        elif signal < 65:
            score += 8

        # Cap score
        score = min(score, 100)

        # ---------------------------
        # Strength classification
        # ---------------------------
        if score >= 70:
            strength = "Very Weak"
            entropy = 15
            crack_days = 1
        elif score >= 50:
            strength = "Weak"
            entropy = 28
            crack_days = 7
        elif score >= 30:
            strength = "Medium"
            entropy = 45
            crack_days = 90
        else:
            strength = "Strong"
            entropy = 70
            crack_days = 365 * 3

        return {
            "strength": strength,
            "entropy_bits": entropy,
            "estimated_crack_days": crack_days,
            "risk_score": score,
            "factors": reasons,
            "recommended_length": 12,
            "has_special_char": True if strength in ["Medium", "Strong"] else False,
            "has_numbers": True if strength != "Very Weak" else False
        }
