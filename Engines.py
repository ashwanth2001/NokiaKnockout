import random
from Presets import *

class Engine():
    def getAction(self, player):
        return 1

class TutorialEngine(Engine):
    def getAction(self, player):
        return 0

class RandomBlocksEngine(Engine):
    def __init__(self):
        super().__init__()
        self.choice = 0
    
    def getAction(self, player):
        if(self.choice == 0):
            self.choice = random.randint(1,16)
            if self.choice > 6:
                self.choice = self.choice%2+1
        if(stamina_costs[self.choice] <  player.stamina):
            choice = self.choice
            self.choice = 0
            return choice
        return 0

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
            
class GoodEngine(Engine):
    def __init__(self):
        super().__init__()
        self.choice = 0
        self.dist = [0, 0, 0, 0.15, 0.15, 0.35, 0.35]
        self.cumsum = [sum(self.dist[0:i]) for i in range(len(self.dist))]
        self.defend = 0
    
    def getAction(self, player):
        if player.enemy.action==0:
            self.defend = 0
        if player.enemy.action>2 and player.enemy.act_idx_dir>0 and player.canAct(1):
            if self.defend==0:
                self.defend = 1 if random.uniform(0, 1)<0.33 else -1
                if self.defend==1:
                    return 1 if player.enemy.action%2==1 else 2
        if self.choice==0:
            r = random.uniform(0, 1)
            for i in range(len(self.cumsum)):
                if r<self.cumsum[i]:
                    return i
        if player.canAct(self.choice):
            action = self.choice
            self.choice = 0
            return action
        return 0