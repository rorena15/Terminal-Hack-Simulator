import sys
import time
import random

def type_text(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class Target:
    def __init__(self, ip, ports, services, vulnerabilities):
        self.ip = ip
        self.open_ports = ports
        self.services = services
        self.vulnerabilities = vulnerabilities
        self.scanned = False
        self.enumerated_ports = []

class Game:
    def __init__(self):
        self.access_level = "none"
        self.trace_level = 0
        self.logs = []
        self.current_level = 1
        self.targets = {
            1: Target("192.168.1.10", [22], {22: "ssh"}, {"ssh": "bruteforce"}),
            2: Target("10.0.5.23", [22, 80], {22: "ssh", 80: "http"}, {"http": "exploit"}),
            3: Target("172.16.42.99", [21, 22, 80], {21: "ftp", 22: "ssh", 80: "http"}, {"ftp": "exploit", "ssh": "bruteforce"})
        }

    def log_action(self, action):
        self.logs.append(action)

    def increase_trace(self, amount):
        self.trace_level += amount
        type_text(f"[!] TRACE 수치 증가: +{amount}% (현재: {self.trace_level}%)")
        if self.trace_level >= 100:
            type_text("\n[!!!] 경고: 시스템에 의해 탐지되었습니다. 연결이 차단됩니다.")
            type_text("=== GAME OVER ===")
            sys.exit()

    def display_status(self):
        print("-" * 40)
        print(f"TARGET IP: {self.targets[self.current_level].ip}")
        print(f"ACCESS LEVEL: {self.access_level.upper()}")
        print(f"TRACE LEVEL: {self.trace_level}%")
        print("-" * 40)

    def run_command(self, cmd_input):
        parts = cmd_input.strip().split()
        if not parts:
            return

        cmd = parts[0].lower()
        target = self.targets[self.current_level]

        if cmd == "help":
            type_text("명령어: scan, enum [port], exploit [service], bruteforce [service], privesc, logs, help")
        elif cmd == "scan":
            type_text("[*] 포트 스캔 중...")
            time.sleep(1)
            target.scanned = True
            type_text(f"[+] 열린 포트 발견: {', '.join(map(str, target.open_ports))}")
            self.log_action("scan 수행")
            self.increase_trace(5)
        elif cmd == "enum":
            if len(parts) < 2:
                type_text("사용법: enum [port]")
                return
            port = int(parts[1])
            if target.scanned and port in target.open_ports:
                type_text(f"[*] 포트 {port} 서비스 분석 중...")
                time.sleep(1)
                service = target.services.get(port)
                target.enumerated_ports.append(port)
                type_text(f"[+] 서비스 확인됨: {port}/tcp -> {service}")
            else:
                type_text("[-] 포트가 닫혀있거나 아직 스캔되지 않았습니다.")
            self.log_action(f"enum {port} 수행")
            self.increase_trace(10)
        elif cmd in ["exploit", "bruteforce"]:
            if len(parts) < 2:
                type_text(f"사용법: {cmd} [service]")
                return
            service = parts[1]
            type_text(f"[*] {service} 서비스에 대해 {cmd} 시도 중...")
            time.sleep(1.5)

            if service in target.services.values() and target.vulnerabilities.get(service) == cmd:
                if random.random() > 0.2:
                    type_text("[+] 공격 성공! USER 권한을 획득했습니다.")
                    self.access_level = "user"
                else:
                    type_text("[-] 공격 실패. 페이로드가 작동하지 않았습니다.")
            else:
                type_text("[-] 해당 서비스에는 이 공격이 유효하지 않습니다.")
            self.log_action(f"{cmd} {service} 수행")
            self.increase_trace(20)
        elif cmd == "privesc":
            if self.access_level == "user":
                type_text("[*] 권한 상승 시도 중...")
                time.sleep(2)
                if random.random() > 0.3:
                    type_text("[+] 권한 상승 성공! ROOT 권한을 획득했습니다.")
                    self.access_level = "root"
                else:
                    type_text("[-] 권한 상승 실패.")
            elif self.access_level == "root":
                type_text("이미 ROOT 권한입니다.")
            else:
                type_text("[-] 권한 상승을 시도하려면 먼저 USER 권한이 필요합니다.")
            self.log_action("privesc 수행")
            self.increase_trace(25)
        elif cmd == "logs":
            type_text("=== 행동 기록 ===")
            for log in self.logs:
                print(f"- {log}")
        else:
            type_text("알 수 없는 명령어입니다. help를 입력하세요.")

    def play(self):
        type_text("=== Terminal Hack Simulator ===")
        type_text("시스템 접속 중...", 0.05)

        while self.current_level <= len(self.targets):
            type_text(f"\n[ MISSION LEVEL {self.current_level} ]")
            self.access_level = "none"
            self.trace_level = 0
            self.logs = []

            while self.access_level != "root":
                self.display_status()
                cmd = input("root@kali:~# ")
                self.run_command(cmd)

            type_text(f"\n[+] 미션 클리어! 시스템 데이터를 탈취했습니다.")
            time.sleep(2)
            self.current_level += 1

        type_text("\n모든 미션을 완료했습니다. 당신은 전설적인 해커입니다!")

if __name__ == "__main__":
    game = Game()
    game.play()