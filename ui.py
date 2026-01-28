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
import os
import pdfkit
from datetime import datetime

st.set_page_config(page_title="Wi-Fi Security Audit Tool", layout="wide")

st.title("🔒 Wi-Fi Security Audit Tool (Lab Simulation)")

# -----------------------------
# Step 1: Adapter Info
# -----------------------------
st.subheader("Step 1: Wireless Adapter Info")
adapter = AdapterManager().detect()
st.write(f"**Adapter:** {adapter['adapter']}")
st.write(f"**Monitor Mode Support:** {adapter['supports_monitor']}")

# -----------------------------
# Step 2: Scan Networks
# -----------------------------
st.subheader("Step 2: Scan Networks")
networks = NetworkScanner().scan()

if not networks:
    st.warning("No networks found.")
    st.stop()

# Display networks in table
import pandas as pd
net_df = pd.DataFrame(networks)
st.dataframe(net_df[["ssid", "bssid", "channel", "signal", "encryption", "vendor", "last_seen"]])

# Network selection
ssid_options = [net["ssid"] for net in networks]
selected_ssid = st.selectbox("Select Target Network", ssid_options)
target = next(net for net in networks if net["ssid"] == selected_ssid)
st.success(f"Selected Network: {target['ssid']}")

# -----------------------------
# Step 3: Encryption Analysis
# -----------------------------
st.subheader("Step 3: Encryption Analysis")
encryption = EncryptionAnalyzer().analyze(target)
st.write(f"**Encryption Type:** {encryption['type']}")
st.write(f"**Severity:** {encryption['severity']}")

# -----------------------------
# Step 4: Handshake Test
# -----------------------------
st.subheader("Step 4: Handshake Test")
handshake = HandshakeTest().run(target)
st.write(f"Handshake Capturable: {handshake['handshake_possible']}")

# -----------------------------
# Step 5: Protection Test
# -----------------------------
st.subheader("Step 5: Protection Features")
protection = ProtectionTest().run(target)
st.write(f"PMF Enabled: {protection['pmf_enabled']}")
st.write(f"WPS Enabled: {protection['wps_enabled']}")

# -----------------------------
# Step 6: Password Audit
# -----------------------------
st.subheader("Step 6: Password Audit")
password = PasswordAudit().run(target)
st.write(f"Strength: {password['strength']}")
st.write(f"Entropy Bits: {password['entropy_bits']}")
st.write(f"Estimated Crack Time (days): {password['estimated_crack_days']}")
st.write("Factors affecting password strength:")
for f in password.get("factors", []):
    st.write(f"- {f}")

# -----------------------------
# Step 7: Risk Assessment
# -----------------------------
st.subheader("Step 7: Risk Assessment")
risk = RiskEngine().calculate(encryption, protection, password)
st.write(f"Risk Level: {risk['level']} ({risk['score']}/15)")

# -----------------------------
# Save Evidence & Generate Report
# -----------------------------
start_time = datetime.now()
st.subheader("Generate Report / Save Evidence")

report_html_path = None
report_pdf_path = None

if st.button("✅ Save Evidence & Generate HTML Report"):
    data = {
        "adapter": adapter,
        "target": target,
        "encryption": encryption,
        "handshake": handshake,
        "protection": protection,
        "password": password,
        "risk": risk,
        "timestamp": start_time.isoformat(),
        "duration": (datetime.now() - start_time).total_seconds()
    }

    # Save evidence
    EvidenceCollector().save(data)

    # Generate HTML report
    report_html_path = ReportGenerator().generate(data)  # Make sure this returns the HTML file path
    st.success(f"✅ Report generated: {report_html_path}")

    # Preview HTML
    with open(report_html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        st.subheader("📄 Report Preview")
        st.components.v1.html(html_content, height=600, scrolling=True)

    # Generate PDF from HTML
    report_pdf_path = report_html_path.replace(".html", ".pdf")
    try:
        pdfkit.from_file(report_html_path, report_pdf_path)
        st.success(f"✅ PDF generated: {report_pdf_path}")
    except Exception as e:
        st.error(f"PDF generation failed: {e}")

    # Download buttons
    with open(report_html_path, "rb") as f:
        st.download_button(
            "⬇️ Download HTML Report",
            f,
            file_name=os.path.basename(report_html_path),
            mime="text/html"
        )

    if report_pdf_path and os.path.exists(report_pdf_path):
        with open(report_pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Download PDF Report",
                f,
                file_name=os.path.basename(report_pdf_path),
                mime="application/pdf"
            )

st.info("⚠️ Note: This tool simulates Wi-Fi auditing in a lab environment only.")