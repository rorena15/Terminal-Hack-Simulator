from systems.trace_system import TraceSystem
from systems.log_system import LogSystem

class Player:
    def __init__(self):
        self.access_level = "none"
        self.money = 500
        self.exp = 0
        self.level = 1
        self.inventory = []
        self.trace = TraceSystem()
        self.log = LogSystem()

    def reset_contract_state(self):
        self.access_level = "none"
        self.trace.reset()
        self.log.reset()
        
        self.trace.stealth_multiplier = 1.0
        if "stealth_pro" in self.inventory:
            self.trace.stealth_multiplier = 0.4
        elif "stealth" in self.inventory:
            self.trace.stealth_multiplier = 0.7

    def promote(self, level):
        self.access_level = level

    def add_reward(self, money, exp):
        self.money += money
        self.exp += exp
        if self.exp >= self.level * 1000:
            self.level += 1
            self.exp = 0
            print(f"\n[!] LEVEL UP! 현재 레벨: {self.level}")

    def apply_penalty(self, penalty_amount):
        self.money -= penalty_amount
        if self.money < 0:
            self.money = 0
        print(f"[-] 추적 회피 및 기록 삭제 비용으로 ${penalty_amount}가 차감되었습니다.")
        print(f"[*] 현재 잔액: ${self.money}")