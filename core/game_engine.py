import sys
from core.player import Player
from core.target import Target
from core.mission import Mission
from systems.shop_system import ShopSystem
from commands import scan, enum, exploit, bruteforce, privesc

class GameEngine:
    def __init__(self):
        self.player = Player()
        self.shop = ShopSystem()
        self.missions = self._init_missions()
        self.mission_commands = {
            "scan": scan.execute,
            "enum": enum.execute,
            "exploit": exploit.execute,
            "bruteforce": bruteforce.execute,
            "privesc": privesc.execute,
            "logs": lambda p, t, a: p.log.show(),
            "abort": self._abort_mission
        }

    def _init_missions(self):
        return {
            1: Mission(1, "초보자 테스트 서버", Target("192.168.1.10", [22], {22: {"name": "ssh", "version": "OpenSSH 5.3"}}, {"ssh": "bruteforce"}, "kernel_exploit"), 500, 500),
            2: Mission(2, "지방 은행 지점망", Target("10.0.5.23", [22, 80], {22: {"name": "ssh", "version": "OpenSSH 7.2"}, 80: {"name": "http", "version": "Apache 2.4.49"}}, {"http": "exploit"}, "suid_bash"), 1200, 1000),
            3: Mission(3, "군사 연구소 외부망", Target("172.16.42.99", [21, 22, 80], {21: {"name": "ftp", "version": "vsftpd 2.3.4"}, 22: {"name": "ssh", "version": "OpenSSH 8.0"}, 80: {"name": "http", "version": "Nginx 1.14"}}, {"ftp": "exploit", "ssh": "bruteforce"}, "cron_job"), 2500, 2000)
        }

    def _abort_mission(self, player, target, args):
        print("[-] 미션을 포기하고 안전하게 연결을 끊습니다.")
        return "abort"

    def run(self):
        print("=== Terminal Hack Simulator : W.O.R.L.D ===")
        while True:
            self._hub_loop()

    def _hub_loop(self):
        print(f"\n[HUB] LV.{self.player.level} | MONEY: ${self.player.money} | EXP: {self.player.exp}")
        print("명령어: shop, buy [item], missions, start [id], info, exit")
        cmd_input = input("hub> ").strip().split()
        
        if not cmd_input:
            return
            
        cmd, *args = cmd_input
        
        if cmd == "shop":
            self.shop.show()
        elif cmd == "buy" and args:
            self.shop.buy(self.player, args[0])
        elif cmd == "missions":
            print("\n=== AVAILABLE MISSIONS ===")
            for m_id, m in self.missions.items():
                status = "[CLEARED]" if m.cleared else "[OPEN]"
                print(f"{m_id}. {m.title} {status} - Reward: ${m.reward_money}")
        elif cmd == "start" and args:
            try:
                m_id = int(args[0])
                if m_id in self.missions and not self.missions[m_id].cleared:
                    self._mission_loop(self.missions[m_id])
                else:
                    print("[-] 유효하지 않거나 이미 클리어한 미션입니다.")
            except ValueError:
                print("[-] 미션 ID를 숫자로 입력하세요.")
        elif cmd == "info":
            print(f"Inventory: {', '.join(self.player.inventory)}")
        elif cmd == "exit":
            sys.exit()

    def _mission_loop(self, mission):
        self.player.reset_mission_state()
        target = mission.target
        print(f"\n[ MISSION START: {mission.title} ]")

        while self.player.access_level != "root":
            if self.player.trace.is_detected():
                print("\n[!!!] 시스템 탐지됨. 연결 차단. 미션 실패.")
                return

            print(f"\nTARGET: {target.ip} | LEVEL: {self.player.access_level.upper()} | TRACE: {self.player.trace.level}%")
            cmd_input = input("root@kali:~# ").strip().split()
            
            if not cmd_input:
                continue
            
            cmd, *args = cmd_input
            if cmd in self.mission_commands:
                result = self.mission_commands[cmd](self.player, target, args)
                if result == "abort":
                    return
            elif cmd == "help":
                print("명령어: scan, enum [port], exploit [service], bruteforce [service], privesc, logs, abort")
            else:
                print("[-] 알 수 없는 명령어입니다.")

        print(f"\n[+] 미션 클리어! 데이터를 탈취했습니다.")
        print(f"[+] 보상 획득: ${mission.reward_money}, EXP: {mission.reward_exp}")
        self.player.add_reward(mission.reward_money, mission.reward_exp)
        mission.cleared = True