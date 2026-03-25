def execute(player, target, args):
    if not args:
        print("사용법: enum [port]")
        return
    
    try:
        port = int(args[0])
    except ValueError:
        print("[-] 유효하지 않은 포트 번호입니다.")
        return

    if not target.state["scanned"]:
        print("[-] 포트 정보가 없습니다. scan을 먼저 수행하세요.")
        return

    if port in target.ports:
        service_info = target.services[port]
        print(f"[*] 포트 {port} 서비스 분석 중...")
        print(f"[+] 발견된 서비스: {service_info['name']} (버전: {service_info['version']})")
        if port not in target.state["enumerated"]:
            target.state["enumerated"].append(port)
        player.trace.increase(10)
        player.log.add(f"enum {port} 수행", f"{service_info['name']} 서비스에 대한 공격 벡터를 찾으세요.")
    else:
        print("[-] 포트가 닫혀있습니다.")
        player.trace.increase(5)