import pygame
from Engines import *
from Presets import *

class Part():
    def __init__(self, loc):
        self.loc = loc
        self.health = 5
        self.kd = 0
    
    def attack(self, dmg):
        if self.health-dmg<=0:
            self.kd+=1
            self.health = 5-self.kd*2
            return 1
        else:
            self.health-=dmg
            return 0


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, facing):
        super().__init__()
        self.move_set = moves if facing==1 else moves_reflect
        self.action = 0
        self.act_idx_dir = 0
        self.act_idx = 0
        
        self.timer = 0

        self.use_text = False 
        self.text_img = None
        self.text_timer = 0
        self.text_y = 0
        
        self.x = x
        self.y = y
        self.facing = facing
        self.offset = 0

        self.stamina = 5
        self.kd = 3
        self.draw_priority = 5

        self.parts = [Part(0), Part(1)]
        self.enemy = None
    
    def setEnemy(self, enemy):
        self.enemy = enemy
    
    def isReady(self):
        return self.act_idx_dir==0
    
    def isAlive(self):
        return self.kd>0

    def canAct(self, event):
        if event.key not in convert:
            return False
        action = convert[event.key]
        if stamina_costs[action]>self.stamina:
            return False
        return True

    def act(self, action):
        self.action = action
        self.act_idx = 0
        self.act_idx_dir = 1
        self.timer = 0
        self.stamina-=stamina_costs[self.action]
    
    def addStamina(self, n):
        self.stamina+=n
        self.stamina = min(self.stamina, stamina_max)

    def takeAttack(self, action):
        dmg = attacks[action][self.action]
        if action==3 and self.action>4:
            '''self.text_timer = 0
            self.text_img = miss_imgs
            self.use_text = True
            self.text_y = 0'''
            return
        elif action>2 and dmg==0 or action>4 and dmg==1:
            '''self.text_timer = 0
            self.text_img = block_imgs
            self.use_text = True
            self.text_y = 0'''
            return
        self.kd -= self.parts[(action+1)%2].attack(dmg)
        self.offset = 0
    
    def takeBlockMiss(self, action):
        dmg = attacks[action][self.action]
        if action==3 and self.action>4:
            self.text_timer = 0
            self.text_img = miss_imgs
            self.use_text = True
            self.text_y = 0
        elif action>2 and dmg==0 or action>4 and dmg==1:
            self.text_timer = 0
            self.text_img = block_imgs
            self.use_text = True
            self.text_y = 0
        else:
            return
        self.kd -= self.parts[(action+1)%2].attack(dmg)
        self.offset = 0

    def moveAttack(self, offset):
        self.offset += offset

    def update(self, elapsed_time):
        if self.action>0 and self.timer == 0 and self.act_idx == len(move_times[self.action]) - 1:
                self.enemy.takeAttack(self.action)
        self.timer += elapsed_time
        self.text_timer += elapsed_time
        offset = 0
        if self.action>0:
            mt = move_times if self.act_idx_dir>0 else reverse_move_times
            if self.timer > mt[self.action][self.act_idx]:
                if(self.act_idx_dir == 1):
                    offset = self.facing*move_offset[self.action][self.act_idx]*-1
                    self.enemy.moveAttack(offset)
                if self.act_idx == len(move_times[self.action]) - 1:
                    self.enemy.takeBlockMiss(self.action)
                    #self.enemy.takeAttack(self.action)                     # TODO make this run at the beginning of the last animation frame
                    self.act_idx_dir = -1
                self.timer = 0
                self.act_idx += self.act_idx_dir
                self.act_idx = max(0, self.act_idx)
            if self.act_idx==0 and self.act_idx_dir==-1:
                self.act_idx = 0
                self.act_idx_dir = 0
                self.action = 0
        else:
            if self.timer>move_times[0][self.act_idx]:
                self.timer = 0
                self.act_idx +=1
                self.act_idx %= len(move_times[0])
        
        if self.use_text:
            self.text_y = -1*int(self.text_timer/50)*SCALE
            if self.text_timer > text_time:
                self.use_text = False
                self.text_timer = 0
                self.text_img = None
        
        return offset

    def draw(self, screen):
        for i in range(self.stamina):
            if self.facing>0:
                screen.blit(stamina_bit_imgs, (4*i*SCALE,0))
        for part in self.parts:
            for i in range(part.health):
                screen.blit(health_bit_imgs,(-14*SCALE*(self.facing-1)+3*i*SCALE,part.loc*7*SCALE))
            for i in range(part.kd):
                screen.blit(health_blackout_imgs,(-14*SCALE*(self.facing-1)-6*i*SCALE,part.loc*7*SCALE))
        screen.blit(self.move_set[self.action][self.act_idx], (self.x+self.offset*SCALE, self.y))

        if self.use_text:
            screen.blit(self.text_img, (-9*SCALE*(self.facing-1), self.text_y))

class Enemy(Player):
    def __init__(self, x, y, facing, engine):
        super().__init__(x, y, facing)
        self.engine = engine
    
    def canAct(self, action):
        if stamina_costs[action]>self.stamina:
            return False
        return True

    def engineAct(self):
        if not self.isReady():
            return
        action = self.engine.getAction(self)
        if not action == 0 and self.canAct(action):
            self.act(action)
    

    
