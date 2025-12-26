import requests
import dns.resolver
import socket

def check_transparent_dns_proxy():
    try:
        # We query a specific trusted server (Quad9)
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['9.9.9.9'] 
        resolver.resolve('google.com', 'A')
        return True, "DNS Direct Connection OK"
    except Exception as e:
        return False, f"Potential DNS Blockage: {str(e)}"

def get_detailed_ip():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=4)
        return r.json()
    except:
        return {}

def get_default_gateway():
    """
    Reads /proc/net/route to find the default gateway IP for each interface.
    Returns: {'eth0': '192.168.1.1', ...}
    """
    gateways = {}
    try:
        with open("/proc/net/route") as f:
            for line in f.readlines()[1:]:
                fields = line.strip().split()
                # Destination 00000000 means Default Route
                if fields[1] == '00000000':
                    iface = fields[0]
                    # Convert Hex to IP
                    gw_hex = fields[2]
                    gw_ip = ".".join(str(int(gw_hex[i:i+2], 16)) for i in range(6, -2, -2))
                    gateways[iface] = gw_ip
    except:
        pass
    return gateways
