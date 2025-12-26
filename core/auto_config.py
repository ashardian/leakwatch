# core/auto_config.py
import socket
import requests
import psutil

def get_physical_interface():
    vpn_patterns = ['tun', 'tap', 'wg', 'ppp', 'proton', 'wireguard']
    stats = psutil.net_if_stats()
    candidates = []
    for iface, stat in stats.items():
        if not stat.isup or iface == "lo": continue
        if any(pat in iface.lower() for pat in vpn_patterns): continue
        candidates.append(iface)
    if candidates: return candidates[0]
    return None

def detect_environment():
    # Removed Dashboard.step()
    phy_iface = get_physical_interface()
    
    active_route_iface = "Unknown"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and addr.address == local_ip:
                    active_route_iface = iface
                    break
    except:
        pass
    
    try:
        ip = requests.get("https://api.ipify.org", timeout=3).text
    except:
        ip = "Unknown"

    return {
        "physical_interface": phy_iface or "Unknown",
        "active_interface": active_route_iface,
        "current_ip": ip
    }
