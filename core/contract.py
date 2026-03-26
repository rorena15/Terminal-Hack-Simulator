class Contract:
    def __init__(self, c_id, title, sec_level, target, reward, penalty):
        self.id = c_id
        self.title = title
        self.sec_level = sec_level
        self.target = target
        self.reward = reward
        self.penalty = penalty
        self.cleared = False