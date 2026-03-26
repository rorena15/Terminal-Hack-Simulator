import sys
from core.player import Player
from core.target import Target
from core.contract import Contract
from systems.shop_system import ShopSystem
from commands import scan, enum, exploit, bruteforce, zero_day, privesc

class GameEngine:
    def __init__(self):
        self.player = Player()
        self.shop = ShopSystem()
        self.contracts = self._init_contracts()
        self.commands = {
            "scan": scan.execute,
            "enum": enum.execute,
            "exploit": exploit.execute,
            "bruteforce": bruteforce.execute,
            "zero_day": zero_day.execute,
            "privesc": privesc.execute,
            "logs": lambda p, t, a: p.log.show(),
            "abort": self._abort_contract
        }

    def _init_contracts(self):
        return {
            1: Contract(1, "개인 NAS 서버 해킹", 1, Target("192.168.0.5", [21], {21: {"name": "ftp", "version": "vsftpd 2.3.4"}}, {"ftp": "bruteforce"}, "weak_perms"), 600, 200),
            2: Contract(2, "스타트업 웹 서버 침투", 2, Target("10.0.5.23", [22, 80], {22: {"name": "ssh", "version": "OpenSSH 7.2"}, 80: {"name": "http", "version": "Apache 2.4.49"}}, {"http": "exploit"}, "suid_bash"), 1500, 500),
            3: Contract(3, "지방 은행 내부망", 3, Target("172.16.42.99", [22, 80, 443], {22: {"name": "ssh", "version": "OpenSSH 8.0"}, 80: {"name": "http", "version": "honeypot"}, 443: {"name": "https", "version": "OpenSSL 1.0.1"}}, {"https": "exploit"}, "cron_job"), 4000, 1500),
            4: Contract(4, "글로벌 기업 메인프레임", 4, Target("10.10.10.50", [22, 445, 3389], {22: {"name": "ssh", "version": "OpenSSH 8.2"}, 445: {"name": "smb", "version": "SMBv3"}, 3389: {"name": "rdp", "version": "Windows RDP"}}, {"smb": "zero_day"}, "kernel_exploit"), 12000, 5000)
        }

    def _abort_contract(self, player, target, args):
        print("[-] 계약을 포기하고 안전하게 연결을 끊습니다.")
        return "abort"

    def run(self):
        print("=== Terminal Hack Simulator : CONTRACTS ===")
        while True:
            self._hub_loop()

    def _hub_loop(self):
        print(f"\n[HUB] LV.{self.player.level} | MONEY: ${self.player.money} | EXP: {self.player.exp}")
        print("명령어: shop, buy [item], board, accept [id], info, exit")
        cmd_input = input("hub> ").strip().split()
        
        if not cmd_input:
            return
            
        cmd, *args = cmd_input
        
        if cmd == "shop":
            self.shop.show()
        elif cmd == "buy" and args:
            self.shop.buy(self.player, args[0])
        elif cmd == "board":
            print("\n=== CONTRACT BOARD ===")
            for c_id, c in self.contracts.items():
                status = "[CLEARED]" if c.cleared else "[OPEN]"
                print(f"{c_id}. {status} [SEC {c.sec_level}] {c.title} (Reward: ${c.reward} / Penalty: -${c.penalty})")
        elif cmd == "accept" and args:
            try:
                c_id = int(args[0])
                if c_id in self.contracts and not self.contracts[c_id].cleared:
                    self._contract_loop(self.contracts[c_id])
                else:
                    print("[-] 유효하지 않거나 이미 완료된 계약입니다.")
            except ValueError:
                print("[-] 계약 ID를 숫자로 입력하세요.")
        elif cmd == "info":
            print(f"Inventory: {', '.join(self.player.inventory) if self.player.inventory else 'Empty'}")
        elif cmd == "exit":
            sys.exit()

    def _contract_loop(self, contract):
        self.player.reset_contract_state()
        target = contract.target
        print(f"\n[ CONTRACT START: {contract.title} | SEC LEVEL: {contract.sec_level} ]")

        while self.player.access_level != "root":
            if self.player.trace.is_detected():
                print("\n[!!!] 보안 시스템에 탐지되었습니다. 강제 연결 해제.")
                print("=== MISSION FAILED ===")
                self.player.apply_penalty(contract.penalty)
                return

            print(f"\nTARGET: {target.ip} | LEVEL: {self.player.access_level.upper()} | TRACE: {self.player.trace.level}%")
            cmd_input = input("root@kali:~# ").strip().split()
            
            if not cmd_input:
                continue
            
            cmd, *args = cmd_input
            if cmd in self.commands:
                result = self.commands[cmd](self.player, target, args)
                if result == "abort":
                    return
            elif cmd == "help":
                print("명령어: scan, enum [port], exploit [service], bruteforce [service], zero_day [service], privesc, logs, abort")
            else:
                print("[-] 알 수 없는 명령어입니다.")

        print(f"\n[+] 계약 완료! 타겟 시스템을 장악했습니다.")
        print(f"[+] 보상 획득: ${contract.reward}, EXP: {contract.reward}")
        self.player.add_reward(contract.reward, contract.reward)
        contract.cleared = True