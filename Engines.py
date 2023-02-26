import random
from Presets import *

class Engine():
    def getAction(self, player):
        return 3

class RandomEngine(Engine):
    def __init__(self):
        super().__init__()
        self.choice = 0
    
    def getAction(self, player):
        if(self.choice == 0):
            self.choice = random.randint(1,6)
        if(stamina_costs[self.choice] <  player.stamina):
            choice = self.choice
            self.choice = 0
            return choice
        return 0
            
