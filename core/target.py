class Target:
    def __init__(self, ip, ports, services, vulnerabilities, privesc_vector):
        self.ip = ip
        self.ports = ports
        self.services = services 
        self.vulnerabilities = vulnerabilities
        self.privesc_vector = privesc_vector
        self.state = {
            "scanned": False,
            "enumerated": []
        }