![LeakWatch Screenshot](https://github.com/ashardian/leakwatch/blob/main/img/assets/screenshot.png)

# 🛡️ LeakWatch v3.0  
### Linux Privacy & Leak Command Center

**LeakWatch** is an advanced, *ops-ready* Linux privacy auditing tool designed for **security researchers, red teamers, journalists, and privacy professionals** operating in hostile or untrusted network environments.

Unlike traditional tools that rely on passive configuration checks, LeakWatch performs **active reconnaissance** across your system’s **kernel, firewall, routing stack, and live network traffic**, culminating in a real-time **wire-tap** of your physical network interface to ensure **no unencrypted traffic escapes your VPN tunnel**.

All of this is presented through a **zero-configuration**, auto-detecting workflow inside a premium **Command Center TUI** (Text User Interface).

---

## 🖥️ Command Center Interface

A persistent, full-screen TUI that displays:

- Identity & geolocation resolution
- Kernel and system hardening audit results
- Firewall kill-switch validation
- Live packet analysis from the physical interface

Built using the **`rich`** library for clear, modern situational awareness.

---

## 🚀 Key Features

### 📡 Active Wire Tap (Military-Grade Leak Detection)

Most tools only check your public IP.  
**LeakWatch attaches a live packet sniffer (Scapy)** directly to your **physical interface** (`eth0`, `wlan0`, etc.) *while your VPN is active*.

**How it works:**
- Monitors outbound packets in real time
- Confirms traffic is encapsulated inside the VPN tunnel

**Smart Filtering**
- Ignores local LAN traffic (`10.x`, `192.168.x`)
- Ignores VM chatter and tunnel-encrypted packets
- Focuses exclusively on *clearnet-bound traffic*

**Leak Detection**
- Any DNS query or TCP/UDP packet exiting the physical interface unencrypted is flagged as a **CRITICAL LEAK**

---

### 🧠 Zero-Config Automation

No flags. No guessing.

On launch, LeakWatch automatically detects:
- Active physical network interface
- VPN / tunnel interface (`tun0`, `wg0`, etc.)
- Real gateway IP
- Current public identity and ASN

---

### 🛡️ Fortress Audit (System Hardening)

Deep inspection of Linux internals that directly impact anonymity:

**Kernel Parameters (`sysctl`)**
- IP forwarding state
- IPv6 global availability
- ICMP redirect acceptance

**Firewall Kill-Switch Validation**
- Audits `iptables` / `nftables`
- Verifies fail-closed behavior if VPN drops

**Transparent Proxy Detection**
- Detects DNS interception and forced redirection by ISP or local networks

---

### 💻 Premium “Cyber-HUD” TUI

Forget scrolling logs.

LeakWatch launches a **full-screen Command Center** with four live panels:

1. **Identity Matrix** – IP, ASN, geo, VPN state  
2. **Network Configuration** – Interfaces, routes, gateways  
3. **Fortress Audit** – Kernel & firewall health  
4. **Live Traffic Feed** – Real-time packet verdicts  

Designed for **instant situational awareness**.

---

## 📦 Installation

### Prerequisites

- Linux OS (Debian, Kali, Ubuntu, Arch, Mint, etc.)
- Python **3.8+**
- **Root privileges**  
  *(required for packet sniffing and reading kernel/firewall configs)*

---

### Setup

Clone the repository:
```bash
git clone https://github.com/ashardian/leakwatch.git
cd leakwatch
```

Install dependencies:
```bash
sudo pip3 install -r requirements.txt
```

---

## ⚔️ Usage

> **Connect to your VPN first**, then run LeakWatch as root.

```bash
sudo python3 main.py
```

### Workflow

1. Tool initializes and auto-calibrates sensors
2. Detected interface and public identity are displayed
3. Command Center launches
4. Diagnostics run sequentially
5. **Active Wire Tap** runs for ~5 seconds
6. Dashboard enters persistent monitoring mode

Press **Ctrl+C** to exit.

---

## 📂 Project Structure

```
leakwatch/
├── assets/
│   └── screenshot.png
├── core/
│   ├── __init__.py
│   ├── auto_config.py
│   ├── firewall.py
│   ├── net_audit.py
│   ├── sys_audit.py
│   └── traffic.py
├── utils/
│   ├── __init__.py
│   └── dashboard.py
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚠️ Disclaimer

This tool is intended **strictly for educational and defensive purposes**.

Root privileges are powerful. Review the code before running with `sudo`.
