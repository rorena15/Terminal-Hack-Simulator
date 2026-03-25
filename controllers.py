import time
import random

class CommandHandler:
    def __init__(self, ui):
        self.ui = ui

    def execute(self, command_str, player, target):
        parts = command_str.strip().split()
        if not parts:
            return

        cmd = parts[0].lower()

        if cmd == "help":
            self._handle_help()
        elif cmd == "scan":
            self._handle_scan(player, target)
        elif cmd == "enum":
            self._handle_enum(parts, player, target)
        elif cmd in ["exploit", "bruteforce"]:
            self._handle_attack(cmd, parts, player, target)
        elif cmd == "privesc":
            self._handle_privesc(player)
        elif cmd == "logs":
            self._handle_logs(player)
        else:
            self.ui.type_text("알 수 없는 명령어입니다. help를 입력하세요.")

    def _handle_help(self):
        self.ui.type_text("명령어: scan, enum [port], exploit [service], bruteforce [service], privesc, logs, help")

    def _handle_scan(self, player, target):
        self.ui.type_text("[*] 포트 스캔 중...")
        time.sleep(1)
        target.scanned = True
        self.ui.type_text(f"[+] 열린 포트 발견: {', '.join(map(str, target.open_ports))}")
        player.log_action("scan 수행")
        player.add_trace(5)

    def _handle_enum(self, parts, player, target):
        if len(parts) < 2:
            self.ui.type_text("사용법: enum [port]")
            return
        port = int(parts[1])
        if target.scanned and port in target.open_ports:
            self.ui.type_text(f"[*] 포트 {port} 서비스 분석 중...")
            time.sleep(1)
            service = target.services.get(port)
            if port not in target.enumerated_ports:
                target.enumerated_ports.append(port)
            self.ui.type_text(f"[+] 서비스 확인됨: {port}/tcp -> {service}")
        else:
            self.ui.type_text("[-] 포트가 닫혀있거나 아직 스캔되지 않았습니다.")
        player.log_action(f"enum {port} 수행")
        player.add_trace(10)

    def _handle_attack(self, attack_type, parts, player, target):
        if len(parts) < 2:
            self.ui.type_text(f"사용법: {attack_type} [service]")
            return
        service = parts[1]
        self.ui.type_text(f"[*] {service} 서비스에 대해 {attack_type} 시도 중...")
        time.sleep(1.5)

        if service in target.services.values() and target.vulnerabilities.get(service) == attack_type:
            if random.random() > 0.2:
                self.ui.type_text("[+] 공격 성공! USER 권한을 획득했습니다.")
                player.access_level = "user"
            else:
                self.ui.type_text("[-] 공격 실패. 페이로드가 작동하지 않았습니다.")
        else:
            self.ui.type_text("[-] 해당 서비스에는 이 공격이 유효하지 않습니다.")
        player.log_action(f"{attack_type} {service} 수행")
        player.add_trace(20)

    def _handle_privesc(self, player):
        if player.access_level == "user":
            self.ui.type_text("[*] 권한 상승 시도 중...")
            time.sleep(2)
            if random.random() > 0.3:
                self.ui.type_text("[+] 권한 상승 성공! ROOT 권한을 획득했습니다.")
                player.access_level = "root"
            else:
                self.ui.type_text("[-] 권한 상승 실패.")
        elif player.access_level == "root":
            self.ui.type_text("이미 ROOT 권한입니다.")
        else:
            self.ui.type_text("[-] 권한 상승을 시도하려면 먼저 USER 권한이 필요합니다.")
        player.log_action("privesc 수행")
        player.add_trace(25)

    def _handle_logs(self, player):
        self.ui.type_text("=== 행동 기록 ===")
        for log in player.logs:
            print(f"- {log}")