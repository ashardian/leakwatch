# core/firewall.py
import subprocess
import shutil

def check_killswitch():
    has_protection = False
    details = []

    if shutil.which("nft"):
        try:
            output = subprocess.check_output(["nft", "list", "ruleset"], text=True)
            if "policy drop" in output or "reject" in output:
                has_protection = True
                details.append("NFTables active")
        except:
            pass

    if shutil.which("iptables"):
        try:
            output = subprocess.check_output(["iptables", "-S", "OUTPUT"], text=True)
            if "-P OUTPUT DROP" in output:
                has_protection = True
                details.append("IPtables DROP policy")
            
            rules = subprocess.check_output(["iptables", "-L", "-n", "-v"], text=True)
            if "tun" in rules or "wg" in rules:
                details.append("Interface rules found")
        except:
            pass

    return has_protection, details
