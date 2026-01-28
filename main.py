# 📄 main.py
from modules.adapter_manager import AdapterManager
from modules.network_scanner import NetworkScanner
from modules.encryption_analyzer import EncryptionAnalyzer
from modules.handshake_test import HandshakeTest
from modules.protection_test import ProtectionTest
from modules.password_audit import PasswordAudit
from modules.risk_engine import RiskEngine
from modules.evidence_collector import EvidenceCollector
from modules.report_generator import ReportGenerator
import yaml
import sys
import os
import time
from datetime import datetime

class WifiAuditTool:
    def __init__(self):
        self.config = self.load_config()
        self.start_time = datetime.now()
        
    def load_config(self):
        try:
            with open("config.yaml", "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print("⚠️  config.yaml not found, using default settings")
            return {}
    
    def verify_authorization(self):
        if not os.path.exists("authorization.txt"):
            print("❌ Authorization file missing. Create authorization.txt with:")
            print("\"I have written authorization to test this Wi-Fi network in a lab environment.\"")
            sys.exit(1)
        
        with open("authorization.txt", "r") as f:
            content = f.read().strip()
            if "authorization" not in content.lower() or "lab" not in content.lower():
                print("❌ Invalid authorization text.")
                sys.exit(1)
        
        print("✅ Authorization verified")
    
    def select_target(self, networks):
        print("\n📡 Available Networks:")
        for i, net in enumerate(networks, 1):
            print(f"{i}. {net['ssid']} ({net['encryption']}) - Signal: {net['signal']}dBm")
        
        if len(networks) == 1:
            return networks[0]
        
        try:
            choice = int(input("\nSelect target network (number): "))
            return networks[choice-1]
        except:
            print("⚠️  Invalid selection, using first network")
            return networks[0]
    
    def run_audit(self):
        print("=" * 50)
        print("🔒 Wi-Fi Security Audit Tool (Lab Simulation)")
        print("=" * 50)
        
        # Step 1: Check adapter
        print("\n[1/7] Checking wireless adapter...")
        adapter = AdapterManager().detect()
        print(f"   Adapter: {adapter['adapter']}")
        print(f"   Monitor Mode: {adapter['supports_monitor']}")
        
        # Step 2: Scan networks
        print("\n[2/7] Scanning for networks...")
        networks = NetworkScanner().scan()
        if not networks:
            print("❌ No networks found in simulation")
            return
        
        target = self.select_target(networks)
        print(f"   Selected: {target['ssid']}")
        
        # Step 3: Analyze encryption
        print("\n[3/7] Analyzing encryption...")
        encryption = EncryptionAnalyzer().analyze(target)
        print(f"   Type: {encryption['type']} → {encryption['severity']}")
        
        # Step 4: Handshake test
        print("\n[4/7] Testing handshake capture...")
        handshake = HandshakeTest().run(target)
        print(f"   Capturable: {handshake['handshake_possible']}")
        
        # Step 5: Protection features
        print("\n[5/7] Checking protection mechanisms...")
        protection = ProtectionTest().run(target)
        print(f"   PMF: {protection['pmf_enabled']}, WPS: {protection['wps_enabled']}")
        
        # Step 6: Password audit
        print("\n[6/7] Auditing password strength...")
        password = PasswordAudit().run(target)
        print(f"   Strength: {password['strength']}")
        
        # Step 7: Risk assessment
        print("\n[7/7] Calculating risk...")
        risk = RiskEngine().calculate(encryption, protection, password)
        print(f"   Risk Level: {risk['level']} ({risk['score']}/15)")
        
        # Compile data
        data = {
            "adapter": adapter,
            "target": target,
            "encryption": encryption,
            "handshake": handshake,
            "protection": protection,
            "password": password,
            "risk": risk,
            "timestamp": self.start_time.isoformat(),
            "duration": (datetime.now() - self.start_time).total_seconds()
        }
        
        # Save evidence
        EvidenceCollector().save(data)
        
        # Generate report
        ReportGenerator().generate(data)
        
        print("\n" + "=" * 50)
        print("✅ Audit completed successfully!")
        print(f"📊 Report saved in /reports directory")
        print("=" * 50)
        
        return data

def main():
    tool = WifiAuditTool()
    tool.verify_authorization()
    tool.run_audit()

if __name__ == "__main__":
    main()