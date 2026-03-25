import sys
import time
from models import Player, Target
from ui import ConsoleUI
from controllers import CommandHandler

class GameManager:
    def __init__(self):
        self.ui = ConsoleUI()
        self.player = Player()
        self.command_handler = CommandHandler(self.ui)
        self.levels = {
            1: Target("192.168.1.10", [22], {22: "ssh"}, {"ssh": "bruteforce"}),
            2: Target("10.0.5.23", [22, 80], {22: "ssh", 80: "http"}, {"http": "exploit"}),
            3: Target("172.16.42.99", [21, 22, 80], {21: "ftp", 22: "ssh", 80: "http"}, {"ftp": "exploit", "ssh": "bruteforce"})
        }
        self.current_level = 1

    def play(self):
        self.ui.type_text("=== Terminal Hack Simulator ===")
        self.ui.type_text("시스템 접속 중...", 0.05)

        while self.current_level <= len(self.levels):
            target = self.levels[self.current_level]
            self.ui.type_text(f"\n[ MISSION LEVEL {self.current_level} ]")
            self.player.reset()

            while self.player.access_level != "root":
                if self.player.trace_level >= 100:
                    self.ui.type_text(f"\n[!] 현재 TRACE 수치: {self.player.trace_level}%")
                    self.ui.type_text("\n[!!!] 경고: 시스템에 의해 탐지되었습니다. 연결이 차단됩니다.")
                    self.ui.type_text("=== GAME OVER ===")
                    sys.exit()

                self.ui.display_status(target.ip, self.player.access_level, self.player.trace_level)
                cmd_input = self.ui.get_input()
                self.command_handler.execute(cmd_input, self.player, target)

            self.ui.type_text(f"\n[+] 미션 클리어! 시스템 데이터를 탈취했습니다.")
            time.sleep(2)
            self.current_level += 1

        self.ui.type_text("\n모든 미션을 완료했습니다. 당신은 전설적인 해커입니다!")