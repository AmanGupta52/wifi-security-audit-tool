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
- Automated security assessment & reporting  

---

## 🏗 Project Architecture

wifi_audit/
│
├── main.py
├── ui.py
├── config.yaml
├── authorization.txt
│
├── modules/
│ ├── adapter_manager.py
│ ├── network_scanner.py
│ ├── encryption_analyzer.py
│ ├── handshake_test.py
│ ├── protection_test.py
│ ├── password_audit.py
│ ├── risk_engine.py
│ ├── evidence_collector.py
│ └── report_generator.py
│
├── templates/
│ └── report.html
│
├── reports/
├── evidence/
└── logs/


---

## ⚙ Technology Stack

| Component | Tool |
|----------|------|
| Language | Python 3.10+ |
| UI | Streamlit |
| Reporting | Jinja2, HTML |
| PDF Export | pdfkit + wkhtmltopdf |
| Data Handling | Pandas, NumPy |
| Config | YAML |
| Visualization (optional) | Matplotlib / Plotly |

---

## 🚀 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/wifi-security-audit-tool.git
cd wifi-security-audit-tool
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/macOS
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run Application
streamlit run ui.py
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
Generated reports include:

Cover page

Adapter details

Network scan results

Encryption analysis

Protection status

Password audit metrics

Risk assessment

Audit duration & timestamp

Security recommendations

Reports are stored in:

/reports
Evidence files in:

/evidence
⚠ Legal & Ethical Disclaimer
This tool is strictly for:

Educational use

Cybersecurity labs

SOC simulations

Authorized testing environments

❌ Do NOT use this tool on networks you do not own or have permission to test.

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
This project is for educational use only. Add your preferred open-source license if needed.