class LogSystem:
    def __init__(self):
        self.logs = []

    def add(self, action, hint=""):
        self.logs.append({"action": action, "hint": hint})

    def show(self):
        print("=== 행동 기록 및 분석 힌트 ===")
        for log in self.logs:
            hint_text = f" -> Hint: {log['hint']}" if log['hint'] else ""
            print(f"- {log['action']}{hint_text}")

    def reset(self):
        self.logs.clear()