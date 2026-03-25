def execute(player, target, args):
    if player.access_level != "user":
        print("[-] 권한 상승을 시도하려면 먼저 USER 권한이 필요합니다.")
        return

    print("[*] 시스템 내부 취약점 스캔 및 권한 상승 시도 중...")
    
    if target.privesc_vector:
        print(f"[+] 내부 취약점({target.privesc_vector}) 발견 및 익스플로잇 성공!")
        print("[+] ROOT 권한을 획득했습니다.")
        player.promote("root")
    else:
        print("[-] 권한 상승 벡터를 찾을 수 없습니다.")
    
    player.trace.increase(25)
    player.log.add("privesc 수행")