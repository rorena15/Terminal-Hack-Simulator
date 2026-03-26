from ui.ui_manager import UIManager

def execute(player, target, args):
    UIManager.show_action("포트 스캔 중...")
    target.state["scanned"] = True
    ports_str = ', '.join(map(str, target.ports))
    UIManager.show_success(f"열린 포트 발견: {ports_str}")
    player.trace.increase(5)
    player.log.add("scan 수행", "열린 포트를 기반으로 enum 명령어를 사용해 서비스를 분석하세요.")