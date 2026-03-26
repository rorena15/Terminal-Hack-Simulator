from ui.ui_manager import UIManager

class TraceSystem:
    def __init__(self):
        self.level = 0
        self.limit = 100
        self.stealth_multiplier = 1.0

    def increase(self, amount):
        actual_amount = int(amount * self.stealth_multiplier)
        self.level += actual_amount
        UIManager.show_warning(f"TRACE 증가: +{actual_amount}% (현재: {self.level}%)")

    def is_detected(self):
        return self.level >= self.limit

    def reset(self):
        self.level = 0