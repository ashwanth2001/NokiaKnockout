from GameController import GameController
from SoundController import SoundController

sound = SoundController()
controller = GameController(sound)
while controller.update():
    sound.update()
    controller.draw()