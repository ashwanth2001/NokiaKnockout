from Player import *
from Presets import *
from MyEnums import *
import pygame

class GameController():
    def __init__(self, sound):
        self.sound = sound

        self.player1 = Player(-4*SCALE, 35*SCALE, 1)
        self.player2 = Enemy(18*SCALE, 35*SCALE, -1, RandomEngine())

        self.player1.setEnemy(self.player2)
        self.player2.setEnemy(self.player1)

        self.player1.setSound(self.sound)
        self.player2.setSound(self.sound)

        self.all_sprites = [self.player1, self.player2]
        self.state = GameState.INTRO
        
        self.screen = surface
        self.clock = pygame.time.Clock()
        
        self.turn = 0
        self.timer = 0
        self.elapsed_time = 0
        self.events = []

        self.intro_flash_tick = 750
        self.intro_flash = False

        self.intro_transition_idx = 0
        self.intro_transition_max = 27
        self.intro_transition_tick = 20

        self.end_transition_tick = 4000
        self.end_finish_animation_tick = 1000
        self.end_flash_tick = 750
        self.end_flash = False
        self.end_timer = 0

        self.shake = False
        self.shake_tick = 20
        self.shake_max = 10
        self.shake_idx = 0

        self.stamina_timer = 0
        self.stamina_tick = 1000
        self.stamina_tick = 1

        self.priority_player = 0
        self.animate_idx = 0

        self.background_position = 0
        self.player_wins = False
        

    def update(self):

        self.elapsed_time = self.clock.tick(frame_rate)
        self.timer+=self.elapsed_time

        self.events = pygame.event.get()

        if self.state == GameState.INTRO:
            self.updateIntro()
        if self.state == GameState.INTRO_TRANSITION:
            self.updateIntroTransition()
        if self.state == GameState.GAME:
            self.updateGame()
        if self.state == GameState.END:
            self.end_timer += self.elapsed_time
            self.updateEnd()
        return True

    def draw(self):
        if self.state == GameState.INTRO:
            self.drawIntro()
        if self.state == GameState.INTRO_TRANSITION:
            self.drawIntroTransition()
        if self.state == GameState.GAME:
            self.drawGame()
        if self.state == GameState.END:
            self.drawEnd()
        pygame.display.flip()
    
    def updateIntro(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.timer = 0
                self.state = GameState.END
            elif event.type == pygame.KEYDOWN:
                self.timer = 0
                self.state = GameState.INTRO_TRANSITION
        if self.timer>self.intro_flash_tick:
            self.intro_flash = not self.intro_flash
            self.timer = 0
    
    def drawIntro(self):
        self.screen.blit(start_screeen_imgs,(0,0))
        if self.intro_flash:
            self.screen.blit(press_to_start_imgs,(0,0))

    def updateEnd(self):
        if self.end_timer > self.end_transition_tick:
            if int(self.end_timer/self.end_flash_tick)%2 == 0:
                self.end_flash = True
            else:
                self.end_flash = False
        else:
            if self.end_timer < self.end_finish_animation_tick:
                self.updateGame()
    
    def drawEnd(self):
        if self.end_timer > self.end_transition_tick:
            index = int(self.background_position/48)
            position = self.background_position - index*48
        
            for i in range(-1, 2):
                self.screen.blit(background_imgs[(index+i)%len(background_imgs)], (i*48*SCALE+position*SCALE,0))
            
            if self.end_flash:
                self.screen.blit(game_over_screen_imgs,(0,0))
        else:
            self.drawGame()
            if self.player_wins:
                self.screen.blit(player_wins_imgs,(0,0))
            else:
                self.screen.blit(enemy_wins_imgs,(0,0))
    
    def updateIntroTransition(self):
        if self.timer > self.intro_transition_tick:
            self.intro_transition_idx+=1
            self.timer = 0
        if self.intro_transition_idx>27:
            self.timer = 0
            self.state = GameState.GAME

    def drawIntroTransition(self):
        self.screen.blit(blank_green_imgs,(0,0))
        self.screen.blit(background_imgs[0],(0,27*SCALE-self.intro_transition_idx*SCALE))
        self.screen.blit(start_screeen_imgs,(0,-self.intro_transition_idx*SCALE))

        self.screen.blit(moves[0][0], (self.player1.x, self.player1.y+27*SCALE-self.intro_transition_idx*SCALE))
        self.screen.blit(moves_reflect[0][0], (self.player2.x, self.player2.y+27*SCALE-self.intro_transition_idx*SCALE))
    
    def updateGame(self):
        if not self.player1.isAlive() or not self.player2.isAlive():
            self.state = GameState.END
            #Check who won
            if self.player1.isAlive():
                self.player_wins = True
            else:
                self.player_wins = False

        offset1 = self.player1.update(self.elapsed_time)
        offset2 = self.player2.update(self.elapsed_time)

        self.background_position += offset1 + offset2
        self.background_position %= len(background_imgs)*48

        self.stamina_timer+=self.elapsed_time

        if self.stamina_timer > self.stamina_tick:
            self.player1.addStamina(1)
            self.player2.addStamina(1)
            self.stamina_timer = 0

        '''if self.shake and self.timer>self.shake_tick:
            self.timer = 0
            self.shake_idx+=1
        if self.shake_idx==self.shake_max:
            self.timer = 0
            self.shake_idx = 0
            self.shake = False'''
        
        for event in self.events:
            if event.type == pygame.QUIT:
                self.timer = 0
                self.state = GameState.END
            elif event.type == pygame.KEYDOWN and self.player1.isReady() and self.player1.canAct(event):
                self.player1.act(convert[event.key])
        
        if self.player2.isReady():
            self.player2.engineAct()
    
    def drawGame(self):
        index = int(self.background_position/48)
        position = self.background_position - index*48
        
        for i in range(-1, 2):
            self.screen.blit(background_imgs[(index+i)%len(background_imgs)], (i*48*SCALE+position*SCALE,0))
        
        self.screen.blit(health_bar_imgs, (0,0))
        self.screen.blit(stamina_bar_imgs, (0,0))

        if not self.player1.isReady():
            self.player2.draw(self.screen)
            self.player1.draw(self.screen)
        else:
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
        




        
        
        
        
