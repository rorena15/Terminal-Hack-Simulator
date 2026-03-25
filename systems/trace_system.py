class TraceSystem:
    def __init__(self):
        self.level = 0
        self.limit = 100

    def increase(self, amount):
        self.level += amount
        print(f"[!] TRACE 수치 증가: +{amount}% (현재: {self.level}%)")

    def is_detected(self):
        return self.level >= self.limit

    def reset(self):
        self.level = 0