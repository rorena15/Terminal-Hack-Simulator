import sys
from core.player import Player
from core.target import Target
from core.contract import Contract
from systems.shop_system import ShopSystem
from ui.ui_manager import UIManager
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
        UIManager.show_error("계약을 포기하고 안전하게 연결을 끊습니다.")
        return "abort"

    def run(self):
        UIManager.type_text("=== Terminal Hack Simulator : CONTRACTS ===", delay=0.03)
        while True:
            self._hub_loop()

    def _hub_loop(self):
        UIManager.show_hud_hub(self.player)
        UIManager.show_info("명령어: shop, buy [item], board, accept [id], info, exit")
        cmd_input = UIManager.get_input("hub")
        
        if not cmd_input:
            return
            
        cmd, *args = cmd_input
        
        if cmd == "shop":
            self.shop.show()
        elif cmd == "buy" and args:
            self.shop.buy(self.player, args[0])
        elif cmd == "board":
            headers = ["ID", "STATUS", "SEC", "TITLE", "REWARD", "PENALTY"]
            rows = [[c_id, "[CLEARED]" if c.cleared else "[OPEN]", f"SEC {c.sec_level}", c.title, f"${c.reward}", f"-${c.penalty}"] for c_id, c in self.contracts.items()]
            UIManager.draw_table("CONTRACT BOARD", headers, rows)
        elif cmd == "accept" and args:
            try:
                c_id = int(args[0])
                if c_id in self.contracts and not self.contracts[c_id].cleared:
                    self._contract_loop(self.contracts[c_id])
                else:
                    UIManager.show_error("유효하지 않거나 이미 완료된 계약입니다.")
            except ValueError:
                UIManager.show_error("계약 ID를 숫자로 입력하세요.")
        elif cmd == "info":
            inv_str = ', '.join(self.player.inventory) if self.player.inventory else 'Empty'
            UIManager.show_info(f"Inventory: {inv_str}")
        elif cmd == "exit":
            sys.exit()

    def _contract_loop(self, contract):
        self.player.reset_contract_state()
        target = contract.target
        UIManager.show_action(f"CONTRACT START: {contract.title} | SEC LEVEL: {contract.sec_level}")

        while self.player.access_level != "root":
            if self.player.trace.is_detected():
                UIManager.show_game_over(contract.penalty)
                self.player.apply_penalty(contract.penalty)
                return

            UIManager.show_hud_mission(self.player, target.ip)
            cmd_input = UIManager.get_input("mission", self.player.access_level, target.ip)
            
            if not cmd_input:
                continue
            
            cmd, *args = cmd_input
            if cmd in self.commands:
                result = self.commands[cmd](self.player, target, args)
                if result == "abort":
                    return
            elif cmd == "help":
                UIManager.show_info("명령어: scan, enum [port], exploit [service], bruteforce [service], zero_day [service], privesc, logs, abort")
            else:
                UIManager.show_error("알 수 없는 명령어입니다.")

        UIManager.show_success("계약 완료! 타겟 시스템을 장악했습니다.")
        UIManager.show_success(f"보상 획득: ${contract.reward}, EXP: {contract.reward}")
        self.player.add_reward(contract.reward, contract.reward)
        contract.cleared = True