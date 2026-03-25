class ShopSystem:
    def __init__(self):
        self.items = {
            "hydra": {"price": 500, "desc": "bruteforce 공격 도구"},
            "metasploit": {"price": 1000, "desc": "exploit 공격 도구"},
            "stealth": {"price": 2000, "desc": "모든 행동의 TRACE 증가량 50% 감소"}
        }

    def show(self):
        print("\n=== DARK WEB MARKET ===")
        for item, info in self.items.items():
            print(f"- {item} : ${info['price']} ({info['desc']})")

    def buy(self, player, item_name):
        if item_name not in self.items:
            print("[-] 존재하지 않는 물품입니다.")
            return

        if item_name in player.inventory:
            print("[-] 이미 보유한 도구입니다.")
            return

        price = self.items[item_name]["price"]
        if player.money >= price:
            player.money -= price
            player.inventory.append(item_name)
            print(f"[+] {item_name} 구매 완료! (잔액: ${player.money})")
        else:
            print("[-] 잔액이 부족합니다.")