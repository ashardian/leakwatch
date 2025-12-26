# utils/dashboard.py
from datetime import datetime
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.console import Group
from rich import box

class HUD:
    def __init__(self):
        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        self.layout["main"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=2)
        )
        self.layout["left"].split_column(
            Layout(name="identity", ratio=1),
            Layout(name="network", ratio=1)
        )
        self.layout["right"].split_column(
            Layout(name="security", ratio=2),
            Layout(name="logs", ratio=1)
        )

        # Initialize Empty States
        self.update_header("SYSTEM INITIALIZED - STANDBY")
        self.update_identity({})
        self.update_network({})
        self.update_security([])
        self.update_logs([])
        self.update_footer("WAITING FOR COMMAND...")

    def update_header(self, status_text):
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[bold cyan]LEAKWATCH v3.0[/] | [white]COMMAND CENTER[/]", 
            f"[dim]{datetime.now().strftime('%H:%M:%S')}[/] | OP: [bold yellow]{status_text}[/]"
        )
        self.layout["header"].update(Panel(grid, style="white on black"))

    def update_identity(self, data):
        table = Table(box=None, expand=True, padding=(0,1))
        table.add_column("METRIC", style="cyan")
        table.add_column("DATA", style="bold white", justify="right")
        
        table.add_row("Public IP", data.get("ip", "---"))
        table.add_row("ISP / Org", data.get("org", "---"))
        table.add_row("City", data.get("city", "---"))
        table.add_row("Region", data.get("region", "---"))
        table.add_row("Country", data.get("country", "---"))
        table.add_row("Timezone", data.get("timezone", "---"))

        self.layout["identity"].update(Panel(
            table, title="[b cyan]IDENTITY MATRIX[/]", border_style="cyan", box=box.ROUNDED
        ))

    def update_network(self, data):
        table = Table(box=None, expand=True, padding=(0,1))
        table.add_column("CONFIG", style="yellow")
        table.add_column("STATE", style="bold white", justify="right")

        table.add_row("Phy. Interface", data.get("physical_interface", "---"))
        table.add_row("Active Route", data.get("active_interface", "---"))
        table.add_row("Gateway IP", data.get("gateway", "---"))
        table.add_row("DNS Proxy", data.get("dns_status", "---"))
        
        self.layout["network"].update(Panel(
            table, title="[b yellow]NETWORK CONFIG[/]", border_style="yellow", box=box.ROUNDED
        ))

    def update_security(self, checks):
        # checks = [(Name, Status, Detail, Color)]
        table = Table(box=box.SIMPLE_HEAD, expand=True, show_edge=False)
        table.add_column("SYSTEM CHECK", ratio=2)
        table.add_column("RESULT", justify="center", ratio=1)
        table.add_column("DETAILS", style="dim", ratio=3)

        for name, status, detail, color in checks:
            table.add_row(name, f"[{color}]{status}[/]", detail)

        self.layout["security"].update(Panel(
            table, title="[b green]FORTRESS AUDIT[/]", border_style="green", box=box.ROUNDED
        ))

    def update_logs(self, logs):
        text = Text()
        for line in logs[-6:]: # Show last 6 lines
            if "CRITICAL" in line or "LEAK" in line:
                text.append(f"✖ {line}\n", style="bold red")
            elif "WARN" in line:
                text.append(f"⚠ {line}\n", style="yellow")
            else:
                text.append(f"✔ {line}\n", style="green")
        
        self.layout["logs"].update(Panel(
            text, title="[b blue]LIVE TRAFFIC FEED[/]", border_style="blue", box=box.ROUNDED
        ))

    def update_footer(self, message, style="white"):
        self.layout["footer"].update(Panel(
            Align.center(f"[bold {style}]{message}[/]"), border_style="grey30"
        ))
