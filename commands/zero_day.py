from systems.exploit_system import ExploitSystem

def execute(player, target, args):
    if "zero_day" not in player.inventory:
        print("[-] 'zero_day' 익스플로잇 코드가 없습니다. 다크웹 상점에서 구하세요.")
        return

    if not args:
        print("사용법: zero_day [service]")
        return

    service = args[0]
    print(f"[*] 미공개 취약점(0-day)을 {service} 서비스에 주입 중...")
    
    result = ExploitSystem.attempt_attack(player, target, "zero_day", service)
    
    if result == "honeypot":
        player.trace.increase(80)
    elif result is True:
        player.promote("user")
        player.trace.increase(10)
    else:
        player.trace.increase(50)