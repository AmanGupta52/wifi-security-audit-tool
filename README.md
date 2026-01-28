# 🔒 Wi-Fi Security Audit Tool (Lab Simulation)

A modular, SOC-style Wi-Fi security auditing framework built in Python to simulate wireless security assessments in a safe lab environment. The tool analyzes encryption standards, protection mechanisms, password strength, and overall network risk, then generates professional HTML/PDF audit reports.

---

## 📌 Features

- 📡 Wireless adapter detection with monitor mode support check
- 🌐 Nearby Wi-Fi network scanning (SSID, BSSID, channel, signal, encryption, vendor)
- 🔐 Encryption analysis (WEP / WPA / WPA2 / WPA3) with severity scoring
- 🤝 Handshake capture feasibility simulation
- 🛡 Protection mechanism checks (PMF, WPS)
- 🔑 Password strength auditing (entropy, crack time, dictionary match)
- ⚠ Risk scoring engine (Low / Medium / High)
- 🧾 Evidence collection in JSON format
- 📄 Professional HTML report generation
- 📥 Optional PDF export support
- 🖥 Interactive SOC-style UI using Streamlit

---

## 🧠 Project Objective

To simulate a full Wi-Fi security audit workflow similar to real SOC operations while ensuring:

- Safe testing in lab environments
- No attacks on real networks
- Educational value for cybersecurity students
- Automated security assessment and reporting

---

## 🏗 Project Architecture

```text
wifi_audit/
│
├── main.py
├── ui.py
├── config.yaml
├── authorization.txt
│
├── modules/
│   ├── adapter_manager.py
│   ├── network_scanner.py
│   ├── encryption_analyzer.py
│   ├── handshake_test.py
│   ├── protection_test.py
│   ├── password_audit.py
│   ├── risk_engine.py
│   ├── evidence_collector.py
│   └── report_generator.py
│
├── templates/
│   └── report.html
│
├── reports/
├── evidence/
└── logs/
⚙ Technology Stack
Component	Tool
Language	Python 3.10+
UI	Streamlit
Reporting	Jinja2, HTML
PDF Export	pdfkit + wkhtmltopdf
Data Handling	Pandas, NumPy
Config	YAML
Visualization (optional)	Matplotlib / Plotly
🚀 How to Run (Windows)
1️⃣ Install Prerequisites
Ensure you have:

✅ Python 3.10+

python --version
✅ Git (optional)

2️⃣ Clone the Project
git clone https://github.com/AmanGupta52/wifi-security-audit-tool.git
cd wifi-security-audit-tool
Or download ZIP and extract manually.

3️⃣ Create Virtual Environment
python -m venv venv
4️⃣ Enable Script Execution (One-time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Press Y to confirm.

5️⃣ Activate Virtual Environment
.\venv\Scripts\Activate.ps1
Expected:

(venv) PS C:\wifi-security-audit-tool>
6️⃣ Install Dependencies
pip install -r requirements.txt
If missing, create requirements.txt:

streamlit
jinja2
pyyaml
pandas
numpy
pdfkit
7️⃣ Run Backend Logic (Optional)
python main.py
8️⃣ Launch Web Interface
streamlit run ui.py
9️⃣ Open in Browser
http://localhost:8501
🔍 Generate Reports (Inside UI)
Select adapter

Scan networks

Run analysis

Click Save Evidence & Generate Report

Outputs:

/reports   → HTML reports
/evidence  → JSON evidence
🧾 Enable PDF Reports (Optional)
Install wkhtmltopdf:

https://wkhtmltopdf.org/downloads.html

Install to:

C:\Program Files\wkhtmltopdf\bin
Verify:

wkhtmltopdf --version
🛠 Common Errors & Fixes
❌ PowerShell execution disabled
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
❌ Streamlit not found
pip install streamlit
❌ Module not found
pip install -r requirements.txt
📊 Workflow
Detect wireless adapter

Scan nearby networks

Analyze encryption

Test handshake feasibility

Check protection mechanisms

Audit password strength

Calculate risk score

Save evidence

Generate HTML/PDF report

📄 Report Output
Includes:

Cover page

Adapter details

Network scan results

Encryption analysis

Protection status

Password audit metrics

Risk assessment

Audit duration & timestamp

Security recommendations

Stored in:

/reports
/evidence
⚠ Legal & Ethical Disclaimer
This tool is strictly for:

Educational use

Cybersecurity labs

SOC simulations

Authorized testing environments

❌ Do NOT use on networks you do not own or have explicit permission to test.

👨‍💻 Author
Aman Gupta
Intern No: 2047

🧾 Resume-Ready Description
Built a SOC-style Wi-Fi security audit tool using Python and Streamlit that simulates wireless security assessments, analyzes encryption protocols, password strength, and protection mechanisms, and generates professional audit reports in HTML/PDF format.

⭐ Future Enhancements
Real packet capture support

Live handshake analysis

ML-based password risk prediction

CVE-based vendor vulnerability lookup

Dashboard charts for risk visualization

Multi-network batch auditing

📜 License
Educational use only. Add an open-source license (MIT / Apache-2.0 / GPL) if required.


---

If you want, I can also:

✅ Add GitHub badges  
✅ Add screenshots section  
✅ Add MIT license file  
✅ Optimize README for recruiters  
✅ Improve UI screenshots section  

Just tell me 👍