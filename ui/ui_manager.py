import sys
import time
import pygame
import os

if os.name == 'nt':
    os.system('')

class Colors:
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    RED = (255, 50, 50)
    WHITE = (220, 220, 220)
    BLACK = (10, 10, 12)
    HUD_BG = (25, 25, 30)

class UIManager:
    _screen = None
    _font = None
    _clock = None
    _lines = []
    _max_lines = 28
    _hud_info = ""
    _hud_color = Colors.CYAN
    _prompt = ""
    _input_text = ""

    @classmethod
    def _ensure_init(cls):
        if cls._screen is None:
            pygame.init()
            cls._screen = pygame.display.set_mode((1024, 768))
            pygame.display.set_caption("Terminal Hack Simulator OS")
            
            # 한글 지원 폰트 리스트 (Windows: 맑은 고딕, Mac: 애플 고딕, Linux: 나눔 고딕)
            font_preferences = ['malgungothic', 'applegothic', 'nanumgothic', 'consolas']
            cls._font = pygame.font.SysFont(font_preferences, 18, bold=True)
            
            cls._clock = pygame.time.Clock()

    @classmethod
    def type_text(cls, text, color=Colors.WHITE, delay=0.01, newline=True):
        cls._ensure_init()
        current_str = ""
        cls._lines.append((current_str, color))
        
        for char in text:
            current_str += char
            cls._lines[-1] = (current_str, color)
            cls._draw_screen()
            if delay > 0:
                pygame.time.wait(int(delay * 1000))
                pygame.event.pump()

    @classmethod
    def show_hud_hub(cls, player):
        cls._hud_info = f" [HUB] LV.{player.level} | MONEY: ${player.money} | EXP: {player.exp} "
        cls._hud_color = Colors.CYAN

    @classmethod
    def show_hud_mission(cls, player, target_ip):
        cls._hud_info = f" [TARGET: {target_ip}] [ACCESS: {player.access_level.upper()}] [TRACE: {player.trace.level}%] "
        cls._hud_color = Colors.RED if player.trace.level > 70 else Colors.YELLOW if player.trace.level > 40 else Colors.GREEN

    @classmethod
    def show_success(cls, text):
        cls.type_text(f"[+] {text}", Colors.GREEN)

    @classmethod
    def show_warning(cls, text):
        cls.type_text(f"[!] {text}", Colors.RED, delay=0.03)

    @classmethod
    def show_action(cls, text):
        cls.type_text(f"[*] {text}", Colors.YELLOW)

    @classmethod
    def show_error(cls, text):
        cls.type_text(f"[-] {text}", Colors.RED)

    @classmethod
    def show_info(cls, text):
        cls.type_text(text, Colors.CYAN, delay=0)

    @classmethod
    def draw_table(cls, title, headers, rows):
        cls.type_text(f"[ {title} ]", Colors.WHITE, delay=0)
        cls.type_text("-" * 80, Colors.CYAN, delay=0)
        header_row = " | ".join(f"{str(h):<12}" for h in headers)
        cls.type_text(header_row, Colors.YELLOW, delay=0)
        cls.type_text("-" * 80, Colors.CYAN, delay=0)
        for row in rows:
            row_str = " | ".join(f"{str(item):<12}" for item in row)
            cls.type_text(row_str, Colors.WHITE, delay=0)
        cls.type_text("-" * 80, Colors.CYAN, delay=0)

    @classmethod
    def show_game_over(cls, penalty):
        cls.type_text("█" * 60, Colors.RED, delay=0)
        cls.type_text("SYSTEM BREACH DETECTED. CONNECTION TERMINATED.", Colors.RED, delay=0.05)
        cls.type_text(f"PENALTY APPLIED: -${penalty}", Colors.RED, delay=0.05)
        cls.type_text("█" * 60, Colors.RED, delay=0)

    @classmethod
    def get_input(cls, context, access_level="none", ip=""):
        cls._ensure_init()
        prompt_color = Colors.CYAN if context == "hub" else Colors.GREEN
        cls._prompt = "hub > " if context == "hub" else f"[{access_level}@{ip}] {'#' if access_level == 'root' else '$'} "
        cls._input_text = ""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        cls._lines.append((cls._prompt + cls._input_text, prompt_color))
                        ret = cls._input_text.strip().split()
                        
                        if ret and ret[0].lower() == "exit":
                            pygame.quit()
                            sys.exit()
                            
                        cls._input_text = ""
                        return ret
                    elif event.key == pygame.K_BACKSPACE:
                        cls._input_text = cls._input_text[:-1]
                    else:
                        cls._input_text += event.unicode
            
            cls._draw_screen(prompt_color)
            cls._clock.tick(60)

    @classmethod
    def _draw_screen(cls, prompt_color=Colors.GREEN):
        cls._screen.fill(Colors.BLACK)
        
        pygame.draw.rect(cls._screen, Colors.HUD_BG, (0, 0, 1024, 50))
        pygame.draw.line(cls._screen, Colors.CYAN, (0, 50), (1024, 50), 2)
        
        if cls._hud_info:
            hud_surface = cls._font.render(cls._hud_info, True, cls._hud_color)
            cls._screen.blit(hud_surface, (20, 15))

        y_offset = 70
        display_lines = cls._lines[-cls._max_lines:]
        for text, color in display_lines:
            text_surface = cls._font.render(text, True, color)
            cls._screen.blit(text_surface, (20, y_offset))
            y_offset += 22
            
        cursor = "_" if time.time() % 1 > 0.5 else ""
        input_surface = cls._font.render(cls._prompt + cls._input_text + cursor, True, prompt_color)
        cls._screen.blit(input_surface, (20, y_offset))
        
        pygame.display.flip()