from Presets import *

class Tutorial():
    def __init__(self):
        self.key_list = ["Q", "A", "W", "S", "E", "D"]
        self.teach_key = 0

        self.teach_tick = 500
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
        
        
