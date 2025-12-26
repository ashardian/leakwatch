import threading
import time
from scapy.all import sniff, IP, UDP, TCP, DNS

class TrafficAnalyzer:
    def __init__(self, physical_iface, vpn_ip=None, duration=5):
        self.iface = physical_iface
        self.vpn_ip = vpn_ip
        self.duration = duration
        self.leaks = []

    def _packet_callback(self, packet):
        if not packet.haslayer(IP):
            return

        dst_ip = packet[IP].dst
        src_ip = packet[IP].src

        # --- SMART FILTER 1: IGNORE LOCAL/LAN TRAFFIC ---
        # 10.x.x.x (VirtualBox/LAN), 192.168.x.x, Multicast
        if (dst_ip.startswith("10.") or 
            dst_ip.startswith("192.168.") or 
            dst_ip.startswith("172.") or 
            dst_ip.startswith("224.") or 
            dst_ip.endswith(".255")):
            return

        # --- SMART FILTER 2: VPN INTEGRITY CHECK ---
        if self.vpn_ip:
            # Safe if destination is the VPN Server
            if dst_ip == self.vpn_ip:
                return 
            
            # Safe if destination is in the same Subnet as VPN Server (Cluster)
            # Example: Exit Node is .137, Entry Node is .134 -> SAFE.
            vpn_subnet = ".".join(self.vpn_ip.split('.')[:3])
            dst_subnet = ".".join(dst_ip.split('.')[:3])
            
            if vpn_subnet == dst_subnet:
                return # Assumed Safe (VPN Cluster Traffic)

            # --- LEAK CONFIRMED ---
            if packet.haslayer(DNS):
                self.leaks.append(f"DNS LEAK: Query to {dst_ip}")
                return

            proto = "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "IP"
            self.leaks.append(f"TRAFFIC LEAK: {proto} to {dst_ip}")

    def start_scan(self):
        try:
            sniff(iface=self.iface, prn=self._packet_callback, timeout=self.duration, store=0)
        except PermissionError:
            return False, ["Error: Root required for sniffing."]
        except Exception as e:
            return False, [f"Sniffer Error: {e}"]
        
        if self.leaks:
            return False, self.leaks
        return True, ["No leaks detected on physical wire."]
