from systems.trace_system import TraceSystem
from systems.log_system import LogSystem

class Player:
    def __init__(self):
        self.access_level = "none"
        self.trace = TraceSystem()
        self.log = LogSystem()

    def reset(self):
        self.access_level = "none"
        self.trace.reset()
        self.log.reset()

    def promote(self, level):
        self.access_level = level