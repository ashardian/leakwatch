🛡️ LeakWatch v3.0 | Linux Privacy & Leak Command Center
An advanced, "Ops-Ready" Linux privacy auditing tool designed for security researchers operating in hostile network environments.

LeakWatch goes beyond passive configuration checks. It performs active reconnaissance on your system's kernel, firewall, and network stack, culminating in a live "wire tap" of your physical network interface to ensure absolutely no unencrypted traffic is escaping your VPN tunnel.

It features a zero-config, auto-detecting workflow presented in a premium "Command Center" TUI (Text User Interface).

🖥️ Command Center Interface
The persistent TUI displaying identity resolution, kernel audit results, and live packet analysis.

🚀 Key Features
📡 Active Wire Tap ("Military-Grade" Check)
Most tools just check your public IP. LeakWatch attaches a packet sniffer (Scapy) to your physical network card (e.g., eth0 or wlan0) while connected to a VPN. It analyzes outgoing packets in real-time.

Smart Filtering: intelligently ignores local LAN traffic (10.x, 192.168.x), VM chatter, and encrypted traffic destined for your VPN server cluster.

Leak Detection: Any DNS query or TCP/UDP packet leaving the physical interface towards the clearnet is immediately flagged as a Critical Leak.

🧠 Zero-Config Automation
No complex flags required. On launch, the tool uses heuristics to automatically detect:

Your active physical interface.

Your VPN/Tunnel interface.

Your real Gateway IP.

Your current public identity.

🛡️ Fortress Audit (System Hardening)
Checks underlying Linux configurations that could compromise anonymity:

Kernel Parameters (sysctl): Audits IP Forwarding, IPv6 global state, and ICMP Redirect acceptance.

Firewall Killswitch: Verifies if iptables or nftables rules exist to block traffic if the VPN connection drops (Fail-Closed).

Transparent Proxy Detection: Detects if your ISP or local network is intercepting and redirecting DNS queries.

💻 Premium "Cyber-HUD" TUI
Forget scrolling text logs. The tool launches a full-screen, persistent dashboard using the rich library, providing instant situational awareness across four panels: Identity Matrix, Network Config, Fortress Audit, and Live Traffic Feed.

📦 Installation
Prerequisites
Linux OS (Debian, Kali, Ubuntu, Arch, etc.)

Python 3.8+

Root Privileges (Required for active packet sniffing and reading restricted kernel/firewall configurations)

Setup
Clone the repository:

Bash

git clone https://github.com/ashardian/leakwatch.git
cd leakwatch
Install dependencies:

Bash

sudo pip3 install -r requirements.txt
⚔️ Usage
Connect to your VPN, then run the tool as root. It will handle the rest.

Bash

sudo python3 main.py
The Workflow:

The tool initializes and auto-calibrates sensors.

It presents the detected target interface and public IP.

Upon confirmation, it launches the full-screen Command Center.

Diagnostics run sequentially. The "Active Wire Tap" runs last for 5 seconds.

Once complete, the dashboard enters persistent monitoring mode. Review the data and press Ctrl+C to exit.

📂 Project Structure
leakwatch/
├── assets/
│   └── screenshot.png       # Image for README
├── core/                    # The Logic Engine (No UI code here)
│   ├── __init__.py
│   ├── auto_config.py       # Heuristics for interface/IP detection
│   ├── firewall.py          # iptables/nftables auditor
│   ├── net_audit.py         # IP geography, DNS proxy, gateway detection
│   ├── sys_audit.py         # Kernel parameter (sysctl) checker
│   └── traffic.py           # Scapy-based active packet sniffer
├── utils/                   # The Visualization Engine
│   ├── __init__.py
│   └── dashboard.py         # The 'rich' layout engine for the TUI
├── main.py                  # The Orchestrator (Connects Core to Utils)
├── requirements.txt         # Python dependencies
└── README.md                # This file
⚠️ Disclaimer
This tool is for educational and defensive purposes only. It is designed to help users verify their own security posture. The authors are not responsible for any misuse or damage caused by this program.

Root privileges are powerful. While this tool is designed to read configurations and sniff packets passively without altering your system, always review code before running it with sudo.
