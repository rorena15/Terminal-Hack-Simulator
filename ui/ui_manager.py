import sys
import time
import os

# Windows 터미널 ANSI 색상 지원 활성화
if os.name == 'nt':
    os.system('')

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class UIManager:
    @staticmethod
    def type_text(text, color=Colors.RESET, delay=0.01, newline=True):
        sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write(Colors.RESET)
        if newline:
            sys.stdout.write('\n')

    @staticmethod
    def show_hud_hub(player):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}[HUB] LV.{player.level} | MONEY: ${player.money} | EXP: {player.exp}{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")

    @staticmethod
    def show_hud_mission(player, target_ip):
        color = Colors.RED if player.trace.level > 70 else Colors.YELLOW if player.trace.level > 40 else Colors.GREEN
        print(f"\n{Colors.CYAN}{'-'*60}{Colors.RESET}")
        print(f"{Colors.BOLD}[TARGET: {target_ip}] [ACCESS: {player.access_level.upper()}] {color}[TRACE: {player.trace.level}%]{Colors.RESET}")
        print(f"{Colors.CYAN}{'-'*60}{Colors.RESET}")

    @staticmethod
    def show_success(text):
        UIManager.type_text(f"[+] {text}", Colors.GREEN)

    @staticmethod
    def show_warning(text):
        UIManager.type_text(f"[!] {text}", Colors.RED, delay=0.03)

    @staticmethod
    def show_action(text):
        UIManager.type_text(f"[*] {text}", Colors.YELLOW)

    @staticmethod
    def show_error(text):
        UIManager.type_text(f"[-] {text}", Colors.RED)

    @staticmethod
    def show_info(text):
        print(f"{Colors.CYAN}{text}{Colors.RESET}")

    @staticmethod
    def draw_table(title, headers, rows):
        print(f"\n{Colors.BOLD}[ {title} ]{Colors.RESET}")
        print(f"{Colors.CYAN}{'-'*60}{Colors.RESET}")
        header_row = " | ".join(f"{str(h):<15}" for h in headers)
        print(f"{Colors.YELLOW}{header_row}{Colors.RESET}")
        print(f"{Colors.CYAN}{'-'*60}{Colors.RESET}")
        for row in rows:
            row_str = " | ".join(f"{str(item):<15}" for item in row)
            print(row_str)
        print(f"{Colors.CYAN}{'-'*60}{Colors.RESET}")

    @staticmethod
    def show_game_over(penalty):
        print(f"\n{Colors.RED}{'█'*60}")
        UIManager.type_text("SYSTEM BREACH DETECTED. CONNECTION TERMINATED.", Colors.BOLD + Colors.RED, 0.05)
        UIManager.type_text(f"PENALTY APPLIED: -${penalty}", Colors.BOLD + Colors.RED, 0.05)
        print(f"{'█'*60}{Colors.RESET}\n")

    @staticmethod
    def get_input(context, access_level="none", ip=""):
        if context == "hub":
            prompt = f"{Colors.CYAN}hub > {Colors.RESET}"
        else:
            symbol = "#" if access_level == "root" else "$"
            prompt = f"{Colors.GREEN}[{access_level}@{ip}] {symbol} {Colors.RESET}"
        return input(prompt).strip().split()