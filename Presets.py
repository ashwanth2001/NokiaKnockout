import pygame
from pygame.locals import *

pygame.init()

frame_rate = 100
SCALE = 10
WIDTH = 48*SCALE
HEIGHT = 84*SCALE
        
flags =  DOUBLEBUF
surface = pygame.display.set_mode([WIDTH, HEIGHT], flags, 16)


health_bar_imgs = pygame.image.load("Images/healthbars.png").convert_alpha()
stamina_bar_imgs = pygame.image.load("Images/staminabar.png").convert_alpha()
stamina_bit_imgs = pygame.image.load("Images/staminabit.png").convert_alpha()
health_bit_imgs = pygame.image.load("Images/healthbit.png").convert_alpha()
health_blackout_imgs = pygame.image.load("Images/healthblackout.png").convert_alpha()
start_screeen_imgs = pygame.image.load("Images/startscreen.png").convert_alpha()
press_to_start_imgs = pygame.image.load("Images/presstostart.png").convert_alpha()
blank_green_imgs = pygame.image.load("Images/blank.png").convert_alpha()
game_over_screen_imgs = pygame.image.load("Images/gameover.png").convert_alpha()
block_imgs = pygame.image.load("Images/block.png").convert_alpha()
miss_imgs = pygame.image.load("Images/miss.png").convert_alpha()
player_wins_imgs = pygame.image.load("Images/playerwins.png").convert_alpha()
enemy_wins_imgs = pygame.image.load("Images/enemywins.png").convert_alpha()

mode_imgs = [
    pygame.image.load("Images/mode_tutorial.png").convert_alpha(),
    pygame.image.load("Images/mode_easy.png").convert_alpha(),
    pygame.image.load("Images/mode_medium.png").convert_alpha(),
    pygame.image.load("Images/mode_hard.png").convert_alpha(),
]

teach_imgs = [
    pygame.image.load("Images/tut_q.png").convert_alpha(),
    pygame.image.load("Images/tut_a.png").convert_alpha(),
    pygame.image.load("Images/tut_w.png").convert_alpha(),
    pygame.image.load("Images/tut_s.png").convert_alpha(),
    pygame.image.load("Images/tut_e.png").convert_alpha(),
    pygame.image.load("Images/tut_d.png").convert_alpha(),
]

background_imgs = [
    pygame.image.load("Images/background_0.png").convert_alpha(),
    pygame.image.load("Images/background_1.png").convert_alpha(),
    pygame.image.load("Images/background_2.png").convert_alpha(),
    pygame.image.load("Images/background_3.png").convert_alpha(),
    pygame.image.load("Images/background_4.png").convert_alpha(),
    pygame.image.load("Images/background_5.png").convert_alpha(),
    pygame.image.load("Images/background_6.png").convert_alpha(),
]

moves = [
    [pygame.image.load("Images/Moves/idle/idle_0.png").convert_alpha(), pygame.image.load("Images/Moves/idle/idle_1.png").convert_alpha()],
    [pygame.image.load("Images/Moves/5/5_0.png").convert_alpha()],
    [pygame.image.load("Images/Moves/6/6_0.png").convert_alpha()],
    [pygame.image.load("Images/Moves/1/1_0.png").convert_alpha(), pygame.image.load("Images/Moves/1/1_1.png").convert_alpha(), pygame.image.load("Images/Moves/1/1_2.png").convert_alpha(), pygame.image.load("Images/Moves/1/1_3.png").convert_alpha()],
    [pygame.image.load("Images/Moves/2/2_0.png").convert_alpha(), pygame.image.load("Images/Moves/2/2_1.png").convert_alpha(), pygame.image.load("Images/Moves/2/2_2.png").convert_alpha()],
    [pygame.image.load("Images/Moves/3/3_0.png").convert_alpha(), pygame.image.load("Images/Moves/3/3_1.png").convert_alpha(), pygame.image.load("Images/Moves/3/3_2.png").convert_alpha(), pygame.image.load("Images/Moves/3/3_3.png").convert_alpha()],
    [pygame.image.load("Images/Moves/4/4_0.png").convert_alpha(), pygame.image.load("Images/Moves/4/4_1.png").convert_alpha(), pygame.image.load("Images/Moves/4/4_2.png").convert_alpha(), pygame.image.load("Images/Moves/4/4_3.png").convert_alpha()],
    [pygame.image.load("Images/Moves/kd/k1_0.png").convert_alpha(), pygame.image.load("Images/Moves/kd/k1_1.png").convert_alpha(), pygame.image.load("Images/Moves/kd/k1_2.png").convert_alpha(), pygame.image.load("Images/Moves/kd/k1_3.png").convert_alpha(), pygame.image.load("Images/Moves/kd/k1_4.png").convert_alpha()],
    [pygame.image.load("Images/Moves/kd/k2_0.png").convert_alpha(), pygame.image.load("Images/Moves/kd/k2_1.png").convert_alpha(), pygame.image.load("Images/Moves/kd/k2_2.png").convert_alpha(), pygame.image.load("Images/Moves/kd/k2_3.png").convert_alpha()]
]

moves_reflect = [[pygame.transform.flip(ci, True, False) for ci in cj] for cj in moves]

move_times = [
    [250, 250],
    [750],
    [750],
    [100, 250, 100, 500],
    [100, 100, 250],
    [100, 100, 100, 500],
    [100, 100, 100, 500],
    [100, 200, 200, 300, 2000],
    [100, 200, 300, 2000],
]

text_time = 250

speed = 1
reverse_speed = 1

reverse_move_times = [[int(ci*reverse_speed) for ci in cj] for cj in move_times]
move_times = [[int(ci*speed) for ci in cj] for cj in move_times]

move_offset = [
    [0, 0],
    [0, 0],
    [0, 0],
    [1, 1, 1, 1],
    [1, 1, 1],
    [0, 2, 3, 2],
    [0, 2, 3, 2],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0],
]

convert = {
    pygame.K_KP7 : 1, # Block
    pygame.K_KP4 : 2,
    pygame.K_KP8 : 3, # Punch
    pygame.K_KP5 : 4, 
    pygame.K_KP9 : 5, # Kick
    pygame.K_KP6 : 6,
    
    pygame.K_q : 1, # Block
    pygame.K_a : 2,
    pygame.K_w : 3, # Punch
    pygame.K_s : 4, 
    pygame.K_e : 5, # Kick
    pygame.K_d : 6
}

attacks = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 1, 1],
    [2, 1, 2, 2, 2, 2, 2],
    [2, 2, 1, 2, 2, 2, 2],
]

stamina_costs = [0, 1, 1, 3, 3, 5, 5]
stamina_max = 9

# Sounds

background_track = "Sounds/back_1.wav"

hit_sfx = "Sounds/hit.wav"
block_sfx = "Sounds/block.wav"
miss_sfx = "Sounds/miss.wav"
kd_sfx = "Sounds/knockdown.wav"

pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])