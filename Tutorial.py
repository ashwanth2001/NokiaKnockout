from Presets import *

class Tutorial():
    def __init__(self):
        self.teach_key = 0

        self.teach_tick = 3000
        self.timer = 0
    
    def draw(self, screen):
        if self.teach_key >= len(teach_imgs):
            return
        screen.blit(teach_imgs[self.teach_key], (0,0))

    def update(self, elapsed_time):
        if self.teach_key >= len(teach_imgs):
            return
        self.timer += elapsed_time
        if self.timer > self.teach_tick:
            self.timer = 0
            self.teach_key += 1
        
        
