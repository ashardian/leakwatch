#!/usr/bin/env python3
import sys
import time
import os
import signal
from rich.live import Live
from rich.prompt import Confirm
from rich.console import Console

# Import Core Modules
try:
    from core import traffic, firewall, net_audit, sys_audit, auto_config
    from utils.dashboard import HUD
except ImportError as e:
    print(f"[!] CRITICAL LOAD ERROR: {e}")
    sys.exit(1)

console = Console()
hud = HUD()

# -- STATE STORAGE --
sec_report = []
log_feed = []
net_data = {}

def add_log(msg):
    ts = time.strftime("%H:%M:%S")
    log_feed.append(f"[{ts}] {msg}")
    hud.update_logs(log_feed)

def add_sec_check(name, passed, detail):
    status = "PASS" if passed else "FAIL"
    color = "bold green" if passed else "bold red"
    sec_report.append((name, status, detail, color))
    hud.update_security(sec_report)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    is_root = os.geteuid() == 0

    try:
        print("[*] Calibrating Sensors...", end="\r")
        config = auto_config.detect_environment()
    except:
        config = {"physical_interface": "Unknown", "current_ip": "Unknown"}

    print(f"\n[+] TARGET INTERFACE: {config.get('physical_interface')}")
    print(f"[+] CURRENT IDENTITY: {config.get('current_ip')}")
    
    if not Confirm.ask("\n[bold yellow]⚠  ENGAGE COMMAND CENTER?[/]"):
        sys.exit()

    with Live(hud.layout, refresh_per_second=4, screen=True):
        
        # --- PHASE 1: IDENTITY ---
        hud.update_header("PHASE 1/4: IDENTITY RECON")
        add_log("Resolving Identity Matrix...")
        idn_data = net_audit.get_detailed_ip() or {}
        hud.update_identity(idn_data)
        
        # Fetch Real Gateway
        gateways = net_audit.get_default_gateway()
        gw_ip = gateways.get(config.get('physical_interface'), "Unknown")

        net_data = {
            "physical_interface": config.get('physical_interface'),
            "active_interface": config.get('active_interface', 'Unknown'),
            "gateway": gw_ip,
            "dns_status": "Scanning..."
        }
        hud.update_network(net_data)
        time.sleep(1)

        # --- PHASE 2: KERNEL ---
        hud.update_header("PHASE 2/4: KERNEL HARDENING")
        add_log("Auditing /proc/sys parameters...")
        warns = sys_audit.check_system_hardening()
        
        add_sec_check("IP Forwarding", "IP Forwarding Enabled" not in warns, "Should be 0")
        add_sec_check("IPv6 Global", "IPv6 Enabled" not in warns, "Kernel IPv6 Active")
        add_sec_check("ICMP Redirects", "ICMP Redirects Accepted" not in warns, "Should be 0")
        time.sleep(0.5)

        # --- PHASE 3: FIREWALL & DNS ---
        hud.update_header("PHASE 3/4: FIREWALL AUDIT")
        
        secure, details = firewall.check_killswitch()
        dtl = details[0] if details else "No Rules Found"
        add_sec_check("Killswitch", secure, dtl)
        
        dns_ok, dns_msg = net_audit.check_transparent_dns_proxy()
        net_data["dns_status"] = "Direct" if dns_ok else "Proxied"
        hud.update_network(net_data)
        add_sec_check("DNS Integrity", dns_ok, dns_msg)
        time.sleep(0.5)

        # --- PHASE 4: ACTIVE SNIFF ---
        hud.update_header("PHASE 4/4: ACTIVE WIRE TAP")
        iface = config.get('physical_interface')
        vpn_ip = config.get('current_ip')

        if is_root and iface and iface != "Unknown":
            add_log(f"Tapping {iface} for 5 seconds...")
            
            secure, sniff_logs = traffic.TrafficAnalyzer(iface, vpn_ip).start_scan()
            
            if secure:
                add_log("Traffic Analysis Complete.")
                add_sec_check("Packet Leak", True, "100% Encrypted")
                hud.update_footer("SYSTEM SECURE | MONITORING ACTIVE", style="green")
            else:
                for l in sniff_logs:
                    add_log(l) # Log leak details
                add_sec_check("Packet Leak", False, f"{len(sniff_logs)} Packets Escaped")
                hud.update_footer("⚠ CRITICAL LEAKS DETECTED ⚠", style="bold red blink")
        else:
            add_log("Skipped Tap (Root Required)")
            add_sec_check("Packet Leak", False, "Skipped")
            hud.update_footer("SCAN COMPLETE (LIMITED)", style="yellow")

        # --- PERSISTENT STATE ---
        hud.update_header("SCAN COMPLETE - PRESS Ctrl+C TO EXIT")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
