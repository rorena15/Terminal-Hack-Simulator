import sys
import time

class ConsoleUI:
    @staticmethod
    def type_text(text, delay=0.02):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    @staticmethod
    def display_status(target_ip, access_level, trace_level):
        print("-" * 40)
        print(f"TARGET IP: {target_ip}")
        print(f"ACCESS LEVEL: {access_level.upper()}")
        print(f"TRACE LEVEL: {trace_level}%")
        print("-" * 40)

    @staticmethod
    def get_input(prompt="root@kali:~# "):
        return input(prompt)