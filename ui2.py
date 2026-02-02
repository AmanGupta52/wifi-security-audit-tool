# ui.py
import streamlit as st
from modules.adapter_manager import AdapterManager
from modules.network_scanner import NetworkScanner
from modules.encryption_analyzer import EncryptionAnalyzer
from modules.handshake_test import HandshakeTest
from modules.protection_test import ProtectionTest
from modules.password_audit import PasswordAudit
from modules.risk_engine import RiskEngine
from modules.evidence_collector import EvidenceCollector
from modules.report_generator import ReportGenerator
from datetime import datetime
import pandas as pd
import time
import os
import tempfile
from datetime import datetime
from modules.password_attack_simulator import WiFiConnector

# Import your existing module
try:
    # Create a wrapper class to handle the WiFi connection simulation
    class WiFiSimulator:
        def __init__(self):
            self.attempt_count = 0
            self.success = False
            self.correct_password = None
            self.logs = []
            
        def test_passwords(self, ssid, passwords):
            """Simulate password testing"""
            self.logs = []
            self.attempt_count = 0
            self.success = False
            self.correct_password = None
            
            # Simulate delays and testing
            total_passwords = len(passwords)
            results = []
            
            for idx, password in enumerate(passwords):
                self.attempt_count += 1
                
                # Add random delay between attempts
                delay = st.session_state.min_delay + idx * 0.5
                time.sleep(min(delay, st.session_state.max_delay))
                
                # Simulate success for demonstration (you can replace with actual logic)
                success = False
                if st.session_state.demo_mode:
                    # In demo mode, succeed on a specific password
                    if password == st.session_state.demo_password:
                        success = True
                
                result = {
                    'attempt': idx + 1,
                    'password': password,
                    'status': 'SUCCESS' if success else 'FAILED',
                    'time': datetime.now().strftime("%H:%M:%S")
                }
                results.append(result)
                
                # Log the attempt
                log_msg = f"[{result['time']}] Attempt {result['attempt']}: '{password}' - {result['status']}"
                self.logs.append(log_msg)
                
                if success:
                    self.success = True
                    self.correct_password = password
                    break
            
            return {
                'success': self.success,
                'password': self.correct_password,
                'attempts': self.attempt_count,
                'logs': self.logs,
                'results': results
            }
    
    wifi_simulator = WiFiSimulator()
    
except ImportError:
    st.error("⚠️ Could not import password_attack_simulator.py")
    # Create a dummy simulator for demo
    class WiFiSimulator:
        def __init__(self):
            self.logs = []
            
        def test_passwords(self, ssid, passwords):
            return {'success': False, 'logs': ["Demo mode active"]}
    
    wifi_simulator = WiFiSimulator()

# Page configuration
st.set_page_config(
    page_title="WiFi Security Tester",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .warning-box {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .password-item {
        background: #f5f5f5;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 4px;
        border-left: 4px solid #2196f3;
        font-family: monospace;
    }
    .log-entry {
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        padding: 0.25rem;
        border-bottom: 1px solid #eee;
    }
    .success-log { color: #4caf50; }
    .error-log { color: #f44336; }
    .info-log { color: #2196f3; }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .progress-container {
        background: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'passwords' not in st.session_state:
    st.session_state.passwords = []
if 'test_results' not in st.session_state:
    st.session_state.test_results = None
if 'target_ssid' not in st.session_state:
    st.session_state.target_ssid = ""
if 'legal_agreement' not in st.session_state:
    st.session_state.legal_agreement = False
if 'min_delay' not in st.session_state:
    st.session_state.min_delay = 3
if 'max_delay' not in st.session_state:
    st.session_state.max_delay = 10
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False
if 'demo_password' not in st.session_state:
    st.session_state.demo_password = "test123"
if 'test_in_progress' not in st.session_state:
    st.session_state.test_in_progress = False

# Header
st.markdown("""
<div class="main-header">
<h1>🛡️ WiFi Security Auditor</h1>
<h3>Simulated Password Strength Testing</h3>
</div>
""", unsafe_allow_html=True)

# Warning Box
st.markdown("""
<div class="warning-box">
<strong>⚠️ LEGAL DISCLAIMER:</strong><br>
This tool is for <strong>EDUCATIONAL PURPOSES ONLY</strong> and should only be used to test 
<strong>YOUR OWN</strong> WiFi networks or networks you have explicit written permission to test. 
Unauthorized access to computer networks is illegal and punishable by law.
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Target Setup", "🔑 Passwords", "⚙️ Settings", "🚀 Run Test"])

# Tab 1: Target Setup
with tab1:
    st.header("1. Target Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.target_ssid = st.text_input(
            "Target WiFi SSID/Name:",
            value=st.session_state.target_ssid,
            placeholder="e.g., MyHomeWiFi"
        )
        
        # Network type selection
        encryption_type = st.selectbox(
            "Encryption Type:",
            ["WPA2-Personal", "WPA3-Personal", "WPA2-Enterprise", "WEP"],
            index=0
        )
    
    with col2:
        # Interface selection (simulated)
        interface = st.selectbox(
            "Network Interface:",
            ["wlan0 (Simulated)", "eth0 (Simulated)", "Wi-Fi (Simulated)"],
            index=0
        )
        
        # Signal strength simulation
        signal_strength = st.slider("Signal Strength:", 0, 100, 85)
        st.progress(signal_strength / 100)
    
    # Legal Agreement
    st.markdown("---")
    st.subheader("Legal Agreement")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="info-box">
        <strong>By checking the box below, you confirm that:</strong><br>
        1. You own the target WiFi network OR have explicit written permission to test it<br>
        2. You understand this is for security testing only<br>
        3. You will not use this tool for unauthorized access
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.session_state.legal_agreement = st.checkbox(
            "I Agree",
            value=st.session_state.legal_agreement
        )
    
    if st.session_state.target_ssid and st.session_state.legal_agreement:
        st.markdown("""
        <div class="success-box">
        ✅ Target configured and legal agreement accepted.
        Proceed to the next tab to add passwords.
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Password Management
with tab2:
    st.header("2. Password List Setup")
    
    # Password input methods
    method = st.radio(
        "Choose password input method:",
        ["Manual Entry", "Text Area", "File Upload"],
        horizontal=True
    )
    
    if method == "Manual Entry":
        col1, col2 = st.columns([3, 1])
        with col1:
            new_password = st.text_input(
                "Enter password:",
                type="password",
                placeholder="Enter password to add"
            )
        with col2:
            if st.button("Add Password", use_container_width=True) and new_password:
                if new_password not in st.session_state.passwords:
                    st.session_state.passwords.append(new_password)
                    st.success(f"Added password #{len(st.session_state.passwords)}")
                else:
                    st.warning("Password already exists in list")
    
    elif method == "Text Area":
        password_text = st.text_area(
            "Enter passwords (one per line):",
            height=150,
            placeholder="password123\ntest1234\nadmin123\n..."
        )
        if st.button("Parse Passwords", use_container_width=True):
            passwords = [p.strip() for p in password_text.split('\n') if p.strip()]
            st.session_state.passwords = list(set(passwords))  # Remove duplicates
            st.success(f"Parsed {len(st.session_state.passwords)} unique passwords")
    
    else:  # File Upload
        uploaded_file = st.file_uploader(
            "Upload password file (TXT or CSV):",
            type=['txt', 'csv']
        )
        if uploaded_file:
            content = uploaded_file.getvalue().decode()
            if uploaded_file.name.endswith('.csv'):
                try:
                    df = pd.read_csv(uploaded_file)
                    if 'password' in df.columns:
                        passwords = df['password'].dropna().astype(str).tolist()
                    else:
                        passwords = content.split('\n')
                except:
                    passwords = content.split('\n')
            else:
                passwords = content.split('\n')
            
            passwords = [p.strip() for p in passwords if p.strip()]
            st.session_state.passwords = list(set(passwords))
            st.success(f"Loaded {len(st.session_state.passwords)} unique passwords from file")
    
    # Display current password list
    st.markdown("---")
    st.subheader(f"Current Password List ({len(st.session_state.passwords)} passwords)")
    
    if st.session_state.passwords:
        # Show first 10 passwords
        for i, pwd in enumerate(st.session_state.passwords[:10]):
            masked = pwd[0] + "*" * (len(pwd) - 2) + (pwd[-1] if len(pwd) > 1 else "")
            st.markdown(f"<div class='password-item'>{i+1}. {masked}</div>", unsafe_allow_html=True)
        
        if len(st.session_state.passwords) > 10:
            st.info(f"Showing 10 of {len(st.session_state.passwords)} passwords")
        
        # Clear button
        if st.button("Clear All Passwords", type="secondary"):
            st.session_state.passwords = []
            st.rerun()
    else:
        st.info("No passwords added yet. Use one of the methods above to add passwords.")

# Tab 3: Settings
with tab3:
    st.header("3. Testing Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Anti-Detection Settings")
        st.session_state.min_delay = st.slider(
            "Minimum delay between attempts (seconds):",
            min_value=1,
            max_value=30,
            value=3,
            help="Prevents router lockout and detection"
        )
        
        st.session_state.max_delay = st.slider(
            "Maximum delay between attempts (seconds):",
            min_value=5,
            max_value=60,
            value=10,
            help="Randomized delay for realism"
        )
        
        max_attempts = st.number_input(
            "Maximum attempts per session:",
            min_value=1,
            max_value=100,
            value=10,
            help="Reset after this many attempts"
        )
    
    with col2:
        st.subheader("Demo Mode")
        st.session_state.demo_mode = st.checkbox(
            "Enable demo mode",
            value=True,
            help="Simulate successful connection with a known password"
        )
        
        if st.session_state.demo_mode:
            st.session_state.demo_password = st.text_input(
                "Demo password (will succeed on this):",
                value="test123",
                type="password"
            )
            st.info("In demo mode, testing will stop when this password is reached")
        
        st.subheader("Output Options")
        save_results = st.checkbox("Save results to file", value=True)
        show_detailed_logs = st.checkbox("Show detailed logs", value=True)

# Tab 4: Run Test
with tab4:
    st.header("4. Execute Security Test")
    
    # Validation checks
    validation_passed = True
    validation_errors = []
    
    if not st.session_state.target_ssid:
        validation_passed = False
        validation_errors.append("❌ Target SSID not set")
    
    if not st.session_state.legal_agreement:
        validation_passed = False
        validation_errors.append("❌ Legal agreement not accepted")
    
    if not st.session_state.passwords:
        validation_passed = False
        validation_errors.append("❌ No passwords added")
    
    # Display validation results
    if validation_errors:
        for error in validation_errors:
            st.error(error)
    
    # Test summary
    if validation_passed:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Target", st.session_state.target_ssid)
        with col2:
            st.metric("Passwords", len(st.session_state.passwords))
        with col3:
            est_time = len(st.session_state.passwords) * (st.session_state.min_delay + 1)
            st.metric("Est. Time", f"{est_time}s")
        
        # Start test button
        if st.button("🚀 Start Security Test", type="primary", use_container_width=True):
            if not st.session_state.test_in_progress:
                st.session_state.test_in_progress = True
                
                # Create progress container
                progress_container = st.empty()
                log_container = st.empty()
                
                with progress_container.container():
                    st.subheader("Test Progress")
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Simulate testing
                    for i in range(len(st.session_state.passwords)):
                        if not st.session_state.test_in_progress:
                            break
                            
                        # Update progress
                        progress = (i + 1) / len(st.session_state.passwords)
                        progress_bar.progress(progress)
                        status_text.text(f"Testing password {i+1}/{len(st.session_state.passwords)}")
                        
                        # Simulate delay
                        time.sleep(0.1)  # Faster for demo
                    
                    # Get results
                    with st.spinner("Finalizing..."):
                        time.sleep(1)
                        results = wifi_simulator.test_passwords(
                            st.session_state.target_ssid,
                            st.session_state.passwords
                        )
                    
                    # Store results
                    st.session_state.test_results = results
                    st.session_state.test_in_progress = False
                    
                    # Clear progress display
                    progress_container.empty()
                    
                    # Show results
                    if results.get('success', False):
                        st.markdown(f"""
                        <div class="success-box">
                        <h3>✅ TEST SUCCESSFUL!</h3>
                        <p><strong>Password found:</strong> {results['password']}</p>
                        <p><strong>Attempts:</strong> {results['attempts']}</p>
                        <p><strong>Target:</strong> {st.session_state.target_ssid}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Download button for results
                        results_text = f"""
                        WiFi Security Test Results
                        =========================
                        Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        Target SSID: {st.session_state.target_ssid}
                        Status: SUCCESS
                        Password Found: {results['password']}
                        Attempts: {results['attempts']}
                        Total Passwords Tested: {len(st.session_state.passwords)}
                        """
                        
                        st.download_button(
                            "📥 Download Results",
                            results_text,
                            file_name=f"wifi_test_{st.session_state.target_ssid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        )
                    else:
                        st.warning("❌ No valid password found in the list")
                        
                        if st.session_state.demo_mode:
                            st.info(f"💡 Demo mode: Would succeed on password '{st.session_state.demo_password}'")
    
    # Test logs
    if st.session_state.test_results and st.session_state.test_results.get('logs'):
        st.markdown("---")
        st.subheader("Test Logs")
        
        log_container = st.container()
        with log_container:
            for log in st.session_state.test_results['logs']:
                log_class = "success-log" if "SUCCESS" in log else "info-log"
                st.markdown(f"<div class='log-entry {log_class}'>{log}</div>", unsafe_allow_html=True)

# Sidebar for quick info
with st.sidebar:
    st.title("Quick Stats")
    
    st.metric("Target SSID", 
              st.session_state.target_ssid if st.session_state.target_ssid else "Not set")
    st.metric("Passwords Loaded", len(st.session_state.passwords))
    
    if st.session_state.test_results:
        st.metric("Last Test Attempts", 
                  st.session_state.test_results.get('attempts', 0))
        if st.session_state.test_results.get('success'):
            st.success("Last test: SUCCESS")
        else:
            st.error("Last test: FAILED")
    
    st.markdown("---")
    st.caption("ℹ️ About this tool:")
    st.caption("This is a simulation tool for educational purposes. It demonstrates how password attacks work without actually connecting to networks.")
    
    if st.button("🔄 Reset All", type="secondary"):
        for key in list(st.session_state.keys()):
            if key not in ['min_delay', 'max_delay', 'demo_mode', 'demo_password']:
                del st.session_state[key]
        st.rerun()

# Footer
st.markdown("---")
st.caption("🔒 **Educational Use Only** | Made for cybersecurity awareness")