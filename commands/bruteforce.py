from systems.exploit_system import ExploitSystem

def execute(player, target, args):
    if "hydra" not in player.inventory:
        print("[-] 'hydra' 도구가 없습니다. 상점에서 구매하세요.")
        return

    if not args:
        print("사용법: bruteforce [service]")
        return

    service = args[0]
    print(f"[*] hydra를 사용하여 {service} 서비스에 대해 bruteforce 시도 중...")
    
    if ExploitSystem.attempt_attack(player, target, "bruteforce", service):
        player.promote("user")
        player.trace.increase(15)
    else:
        player.trace.increase(30)