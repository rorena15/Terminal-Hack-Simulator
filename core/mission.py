class Mission:
    def __init__(self, m_id, title, target, reward_money, reward_exp):
        self.id = m_id
        self.title = title
        self.target = target
        self.reward_money = reward_money
        self.reward_exp = reward_exp
        self.cleared = False