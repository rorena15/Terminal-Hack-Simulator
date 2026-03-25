from systems.exploit_system import ExploitSystem

def execute(player, target, args):
    if not args:
        print("사용법: bruteforce [service]")
        return

    service = args[0]
    print(f"[*] {service} 서비스에 대해 bruteforce 시도 중...")
    
    if ExploitSystem.attempt_attack(player, target, "bruteforce", service):
        player.promote("user")
    
    player.trace.increase(20)