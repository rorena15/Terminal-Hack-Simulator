class Player:
    def __init__(self):
        self.access_level = "none"
        self.trace_level = 0
        self.logs = []

    def add_trace(self, amount):
        self.trace_level += amount

    def log_action(self, action):
        self.logs.append(action)

    def reset(self):
        self.access_level = "none"
        self.trace_level = 0
        self.logs.clear()

class Target:
    def __init__(self, ip, ports, services, vulnerabilities):
        self.ip = ip
        self.open_ports = ports
        self.services = services
        self.vulnerabilities = vulnerabilities
        self.scanned = False
        self.enumerated_ports = []