# modules/network_scanner.py
import subprocess
import re
import yaml
import os
from datetime import datetime

class NetworkScanner:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "config.yaml")

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.simulation = self.config.get("lab_settings", {}).get("simulation_mode", False)

    def scan(self):
        if self.simulation:
            return self._scan_simulated()
        else:
            return self._scan_windows_real()

    # ===============================
    # REAL WINDOWS WIFI SCANNER
    # ===============================
    def _scan_windows_real(self):
        print("\n📡 Scanning real Wi-Fi networks (Windows)...\n")

        cmd = ["netsh", "wlan", "show", "networks", "mode=bssid"]
        output = subprocess.check_output(cmd, shell=True, text=True, encoding="utf-8", errors="ignore")

        networks = []
        current = {}

        for line in output.splitlines():
            line = line.strip()

            if line.startswith("SSID "):
                if current:
                    networks.append(current)

                ssid = line.split(":", 1)[1].strip()
                current = {
                    "ssid": ssid,
                    "bssid": None,
                    "channel": None,
                    "signal": None,
                    "encryption": None,
                    "vendor": None,
                    "last_seen": datetime.now().strftime("%H:%M:%S")
                }

            elif line.startswith("BSSID"):
                bssid = line.split(":", 1)[1].strip()
                current["bssid"] = bssid
                current["vendor"] = self.get_vendor_from_bssid(bssid)

            elif line.startswith("Signal"):
                signal = line.split(":", 1)[1].strip().replace("%", "")
                current["signal"] = int(signal)

            elif line.startswith("Channel"):
                current["channel"] = int(line.split(":", 1)[1].strip())

            elif line.startswith("Authentication"):
                current["encryption"] = line.split(":", 1)[1].strip()

        if current:
            networks.append(current)

        if not networks:
            print("❌ No Wi-Fi networks detected.")
        else:
            for i, n in enumerate(networks, 1):
                print(f"{i}. {n['ssid']} | {n['encryption']} | Signal: {n['signal']}%")

        return networks

    # ===============================
    # SIMULATION MODE (your original)
    # ===============================
    def _scan_simulated(self):
        networks = [
            {
                "ssid": "LabNet",
                "bssid": "AA:BB:CC:DD:EE:FF",
                "channel": 6,
                "signal": -45,
                "encryption": "WPA2",
                "vendor": "Cisco",
                "last_seen": datetime.now().strftime("%H:%M:%S")
            },
            {
                "ssid": "Guest_WiFi",
                "bssid": "11:22:33:44:55:66",
                "channel": 1,
                "signal": -65,
                "encryption": "WPA",
                "vendor": "TP-Link",
                "last_seen": datetime.now().strftime("%H:%M:%S")
            }
        ]

        return networks

    # ===============================
    # VENDOR LOOKUP
    # ===============================
    def get_vendor_from_bssid(self, bssid):
        if not bssid:
            return "Unknown"

        vendor_map = {
            "AA:BB:CC": "Cisco Systems",
            "11:22:33": "TP-Link",
            "AA:11:BB": "Ubiquiti",
            "00:50:F2": "Microsoft",
            "00:1A:2B": "Netgear"
        }

        prefix = bssid[:8].upper()
        return vendor_map.get(prefix, "Unknown")
