# core/sys_audit.py

def _read_sysctl(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return None

def check_system_hardening():
    warnings = []
    
    # 1. IP Forwarding
    if _read_sysctl("/proc/sys/net/ipv4/ip_forward") == "1":
        warnings.append("IP Forwarding Enabled")

    # 2. IPv6 Global State
    if _read_sysctl("/proc/sys/net/ipv6/conf/all/disable_ipv6") == "0":
        warnings.append("IPv6 Enabled")

    # 3. ICMP Redirects
    if _read_sysctl("/proc/sys/net/ipv4/conf/all/accept_redirects") == "1":
        warnings.append("ICMP Redirects Accepted")

    return warnings

def check_routing_table():
    # Simplification: main.py doesn't strictly need this return for the HUD
    # but we keep the function to avoid ImportError if main imports it.
    pass
