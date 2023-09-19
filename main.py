from turtle import Turtle, Screen
from player import Player
from invader_manager import InvaderManager
import time

# initialize turtle Screen instance
screen = Screen()
screen.bgcolor("black")
screen.setup(width=1200, height=1000)
screen.tracer(0)

# initialize gameplay objects
player = Player()
invader_manager = InvaderManager()

# listen for player key presses
screen.listen()
screen.onkey(fun=player.move_left, key="Left")
screen.onkey(fun=player.move_right, key="Right")
screen.onkey(fun=player.shoot, key="space")

# gameplay
invader_manager.create_invaders()

game_on = True
while game_on:
    screen.update()
    time.sleep(0.1)

    # player laser logic
    for laser in player.all_lasers:
        laser.forward(30)
        if laser.ycor() >= 500:
            laser.hideturtle()
            player.all_lasers.remove(laser)


# end program
screen.exitonclick()
