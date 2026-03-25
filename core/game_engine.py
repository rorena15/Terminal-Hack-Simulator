import sys
from core.player import Player
from core.target import Target
from commands import scan, enum, exploit, bruteforce, privesc

class GameEngine:
    def __init__(self):
        self.player = Player()
        self.levels = self._init_levels()
        self.current_level = 1
        self.commands = {
            "scan": scan.execute,
            "enum": enum.execute,
            "exploit": exploit.execute,
            "bruteforce": bruteforce.execute,
            "privesc": privesc.execute,
            "logs": self._show_logs
        }

    def _init_levels(self):
        return {
            1: Target("192.168.1.10", [22], {22: {"name": "ssh", "version": "OpenSSH 5.3"}}, {"ssh": "bruteforce"}, "kernel_exploit"),
            2: Target("10.0.5.23", [22, 80], {22: {"name": "ssh", "version": "OpenSSH 7.2"}, 80: {"name": "http", "version": "Apache 2.4.49"}}, {"http": "exploit"}, "suid_bash"),
            3: Target("172.16.42.99", [21, 22, 80], {21: {"name": "ftp", "version": "vsftpd 2.3.4"}, 22: {"name": "ssh", "version": "OpenSSH 8.0"}, 80: {"name": "http", "version": "Nginx 1.14"}}, {"ftp": "exploit", "ssh": "bruteforce"}, "cron_job")
        }

    def _show_logs(self, player, target, args):
        player.log.show()

    def run(self):
        print("=== Terminal Hack Simulator ===")
        while self.current_level <= len(self.levels):
            target = self.levels[self.current_level]
            self.player.reset()
            print(f"\n[ MISSION LEVEL {self.current_level} ]")

            while self.player.access_level != "root":
                if self.player.trace.is_detected():
                    print("\n[!!!] 시스템 탐지됨. 연결 차단. GAME OVER")
                    sys.exit()

                print(f"\nTARGET: {target.ip} | LEVEL: {self.player.access_level.upper()} | TRACE: {self.player.trace.level}%")
                cmd_input = input("root@kali:~# ").strip().split()
                
                if not cmd_input:
                    continue
                
                cmd, *args = cmd_input
                if cmd in self.commands:
                    self.commands[cmd](self.player, target, args)
                elif cmd == "help":
                    print("명령어: scan, enum [port], exploit [service], bruteforce [service], privesc, logs")
                else:
                    print("알 수 없는 명령어입니다.")

            print("\n[+] 미션 클리어! 시스템 데이터를 탈취했습니다.")
            self.current_level += 1

        print("\n모든 미션을 완료했습니다.")