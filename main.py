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
        invader_manager.invaders_turn()
        start_time = datetime.now()

    # player laser logic
    for laser in player.all_lasers:
        laser.forward(player.laser_speed)
        for invader in invader_manager.all_invaders:
            if laser.distance(invader) < 23:
                invader_manager.all_invaders.remove(invader)
                invader.hideturtle()
                laser.hideturtle()
                player.all_lasers.remove(laser)
        if laser.ycor() >= 500:
            laser.hideturtle()
            player.all_lasers.remove(laser)

    # invader laser logic
    for invader_laser in invader_manager.all_invader_lasers:
        invader_laser.forward(invader_laser.laser_speed)
        if invader_laser.ycor() <= -580:
            invader_laser.hideturtle()
            invader_manager.all_invader_lasers.remove(invader_laser)


# end program
screen.exitonclick()
