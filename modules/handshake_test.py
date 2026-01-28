# 📄 modules/handshake_test.py
import random

class HandshakeTest:
    def run(self, network):
        encryption = network.get("encryption", "WPA2")
        signal = network.get("signal", -50)
        
        # Calculate feasibility based on signal and encryption
        if signal > -40:
            capture_time = random.randint(5, 15)
            success_chance = 0.95
        elif signal > -60:
            capture_time = random.randint(15, 30)
            success_chance = 0.80
        else:
            capture_time = random.randint(30, 60)
            success_chance = 0.50
        
        # Adjust for encryption type
        if encryption == "WPA3":
            success_chance *= 0.3  # Harder for WPA3
        elif encryption == "WPA2":
            success_chance *= 0.8
        elif encryption == "WPA":
            success_chance *= 0.9
        elif encryption == "WEP":
            success_chance = 1.0  # Easy for WEP
        
        return {
            "handshake_possible": random.random() < success_chance,
            "time_seconds": capture_time,
            "packet_count": random.randint(100, 1000),
            "success_probability": round(success_chance * 100, 1),
            "recommended_tools": ["aircrack-ng", "hashcat"] if encryption in ["WPA", "WPA2"] else ["specific tools"],
            "notes": "Simulated handshake capture test"
        }