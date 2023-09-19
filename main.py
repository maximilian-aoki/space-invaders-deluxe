from turtle import Screen
from player import Player
from invader_manager import InvaderManager
from datetime import datetime
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
screen.onkeypress(fun=player.move_left, key="Left")
screen.onkeypress(fun=player.move_right, key="Right")
screen.onkeypress(fun=player.shoot, key="space")

# artificial timer
start_time = datetime.now()

# gameplay
invader_manager.create_invaders()

game_on = True
while game_on:
    screen.update()
    time.sleep(0.1)

    # invader move logic
    time_check = (datetime.now() - start_time).total_seconds()
    if time_check >= invader_manager.move_time:
        invader_manager.move_invaders()
        start_time = datetime.now()

    # player laser logic
    for laser in player.all_lasers:
        laser.forward(player.laser_speed)
        if laser.ycor() >= 500:
            laser.hideturtle()
            player.all_lasers.remove(laser)


# end program
screen.exitonclick()
