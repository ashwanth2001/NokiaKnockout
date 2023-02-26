from GameController import GameController

controller = GameController()
while controller.update():
    controller.draw()