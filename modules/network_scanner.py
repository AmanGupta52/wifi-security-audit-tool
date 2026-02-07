# modules/network_scanner.py

import subprocess
import re
import yaml
import os
import json
import csv
import ctypes

from datetime import datetime


class NetworkScanner:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "config.yaml")

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.simulation = self.config.get("lab_settings", {}).get("simulation_mode", False)

        self.export_dir = os.path.join(base_dir, "reports")
        os.makedirs(self.export_dir, exist_ok=True)

    def scan(self):
        if self.simulation:
            networks = self._scan_simulated()
        else:
            networks = self._scan_windows_real()

        self.export_json(networks)
        self.export_csv(networks)

        return networks

    # ===============================
    # WINDOWS PREFLIGHT CHECK
    # ===============================
    def _windows_precheck(self):
        # ---- Admin privilege check ----
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            is_admin = False

        if not is_admin:
            raise PermissionError(
                "Administrator privileges required.\n"
                "Right-click PowerShell → Run as administrator."
            )

        # ---- WLAN + Location permission check ----
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if "Location permission" in result.stdout:
            # Optional: open settings page (cannot auto-enable)
            # subprocess.run(["start", "ms-settings:privacy-location"], shell=True)

            raise PermissionError(
                "Location Services are disabled.\n"
                "Enable:\n"
                "Settings → Privacy & Security → Location\n"
                "Also enable: 'Let desktop apps access location'."
            )

    # ===============================
    # REAL WINDOWS WIFI SCANNER
    # ===============================
    def _scan_windows_real(self):
        # Mandatory precheck
        self._windows_precheck()

        print("\n📡 Scanning real Wi-Fi networks (Windows)...\n")

        cmd = ["netsh", "wlan", "show", "networks", "mode=bssid"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if result.returncode != 0:
            raise RuntimeError("Wi-Fi scan failed. Ensure WLAN service is running.")

        output = result.stdout

        networks = {}
        current_ssid = None
        current_bssid = None

        for line in output.splitlines():
            line = line.strip()

            if line.startswith("SSID "):
                ssid = line.split(":", 1)[1].strip()
                current_ssid = ssid

                if ssid not in networks:
                    networks[ssid] = {
                        "ssid": ssid,
                        "encryption": None,
                        "bssids": [],
                        "last_seen": datetime.now().strftime("%H:%M:%S")
                    }

            elif line.startswith("Authentication") and current_ssid:
                raw = line.split(":", 1)[1].strip()
                networks[current_ssid]["encryption"] = self.normalize_encryption(raw)

            elif line.startswith("BSSID") and current_ssid:
                bssid = line.split(":", 1)[1].strip()
                current_bssid = {
                    "bssid": bssid,
                    "vendor": self.get_vendor_from_bssid(bssid),
                    "signal": None,
                    "channel": None,
                    "band": None
                }
                networks[current_ssid]["bssids"].append(current_bssid)

            elif line.startswith("Signal") and current_bssid:
                current_bssid["signal"] = self.extract_number(line)

            elif line.startswith("Channel") and current_bssid:
                channel = self.extract_number(line)
                current_bssid["channel"] = channel
                current_bssid["band"] = self.detect_band(channel)

        result = list(networks.values())

        if not result:
            print("❌ No Wi-Fi networks detected.")
        else:
            for i, n in enumerate(result, 1):
                print(f"{i}. {n['ssid']} | {n['encryption']} | APs: {len(n['bssids'])}")

        return result

    # ===============================
    # HELPERS
    # ===============================
    def extract_number(self, text):
        match = re.search(r"\d+", text)
        return int(match.group()) if match else None

    def detect_band(self, channel):
        if channel is None:
            return "Unknown"
        return "2.4 GHz" if channel <= 14 else "5 GHz"

    def normalize_encryption(self, auth):
        auth = auth.lower()

        if "open" in auth:
            return "Open"
        if "wpa3" in auth and "wpa2" in auth:
            return "WPA2/WPA3"
        if "wpa3" in auth:
            return "WPA3"
        if "wpa2" in auth:
            return "WPA2"
        if "wpa" in auth:
            return "WPA"

        return "Unknown"

    # ===============================
    # EXPORT FUNCTIONS
    # ===============================
    def export_json(self, networks):
        path = os.path.join(self.export_dir, "wifi_scan.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(networks, f, indent=4)
        print(f"📄 JSON report saved: {path}")

    def export_csv(self, networks):
        path = os.path.join(self.export_dir, "wifi_scan.csv")

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "SSID", "Encryption", "BSSID", "Vendor", "Signal (%)", "Channel", "Band", "Last Seen"
            ])

            for net in networks:
                for ap in net["bssids"]:
                    writer.writerow([
                        net["ssid"],
                        net["encryption"],
                        ap["bssid"],
                        ap["vendor"],
                        ap["signal"],
                        ap["channel"],
                        ap["band"],
                        net["last_seen"]
                    ])

        print(f"📄 CSV report saved: {path}")

    # ===============================
    # SIMULATION MODE
    # ===============================
    def _scan_simulated(self):
        return [
            {
                "ssid": "LabNet",
                "encryption": "WPA2",
                "bssids": [
                    {
                        "bssid": "AA:BB:CC:DD:EE:FF",
                        "vendor": "Cisco",
                        "signal": 78,
                        "channel": 6,
                        "band": "2.4 GHz"
                    }
                ],
                "last_seen": datetime.now().strftime("%H:%M:%S")
            }
        ]

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
