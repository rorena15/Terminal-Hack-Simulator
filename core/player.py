from systems.trace_system import TraceSystem
from systems.log_system import LogSystem

class Player:
    def __init__(self):
        self.access_level = "none"
        self.money = 500
        self.exp = 0
        self.level = 1
        self.inventory = ["nmap"]
        self.trace = TraceSystem()
        self.log = LogSystem()

    def reset_mission_state(self):
        self.access_level = "none"
        self.trace.reset()
        self.log.reset()
        self.trace.stealth_multiplier = 0.5 if "stealth" in self.inventory else 1.0

    def promote(self, level):
        self.access_level = level

    def add_reward(self, money, exp):
        self.money += money
        self.exp += exp
        if self.exp >= self.level * 1000:
            self.level += 1
            self.exp = 0
            print(f"\n[!] LEVEL UP! 현재 레벨: {self.level}")