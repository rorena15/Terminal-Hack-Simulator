def execute(player, target, args):
    print("[*] 포트 스캔 중...")
    target.state["scanned"] = True
    print(f"[+] 열린 포트 발견: {', '.join(map(str, target.ports))}")
    player.trace.increase(5)
    player.log.add("scan 수행", "열린 포트를 기반으로 enum 명령어를 사용해 서비스를 분석하세요.")