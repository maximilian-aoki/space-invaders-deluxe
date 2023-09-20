from turtle import Screen
from player import Player
from invader_manager import InvaderManager
from barricade_manager import BarricadeManager
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
barricade_manager = BarricadeManager()

# listen for player key presses
screen.listen()
screen.onkeypress(fun=player.move_left, key="Left")
screen.onkeypress(fun=player.move_right, key="Right")
screen.onkeypress(fun=player.shoot, key="space")

# artificial timer
start_time = datetime.now()

# initialize all invaders
invader_manager.create_invaders()
eliminated_list = []


# GAMEPLAY
game_on = True
while game_on:
    screen.update()
    time.sleep(0.1)

    # reset colors after hits
    player.color("white")
    for item in eliminated_list:
        eliminated_list.remove(item)
        item.hideturtle()

    # invaders move and shoot turn
    time_check = (datetime.now() - start_time).total_seconds()
    if time_check >= invader_manager.move_time:
        invader_manager.invaders_turn()
        start_time = datetime.now()

    # player lasers move
    for laser in player.all_lasers:
        laser.forward(player.laser_speed)

        # if laser hits invader
        for invader in invader_manager.all_invaders:
            if laser.distance(invader) <= 23:
                invader_manager.all_invaders.remove(invader)
                player.all_lasers.remove(laser)
                laser.hideturtle()

                # just for a nice UI experience
                eliminated_list.append(invader)
                invader.color("LightGreen")
                break

        # if laser hits barricade
        for block in barricade_manager.all_blocks:
            if laser.distance(block) <= 20:
                barricade_manager.all_blocks.remove(block)
                player.all_lasers.remove(laser)
                laser.hideturtle()

                # just for a nice UI experience
                eliminated_list.append(block)
                block.color("LightGreen")
                break

        # if laser flies off-screen
        if laser.ycor() >= 500:
            laser.hideturtle()
            player.all_lasers.remove(laser)

    # INVADER LASER MOVE
    for invader_laser in invader_manager.all_invader_lasers:
        invader_laser.forward(invader_laser.laser_speed)

        # if laser collides with player laser
        for laser in player.all_lasers:
            if (laser.xcor() >= invader_laser.xcor() - 1) and (laser.xcor() <= invader_laser.xcor() + 1):
                if laser.ycor() >= invader_laser.ycor():
                    player.all_lasers.remove(laser)
                    invader_manager.all_invader_lasers.remove(invader_laser)
                    laser.hideturtle()
                    invader_laser.hideturtle()

        # if laser hits barricade
        for block in barricade_manager.all_blocks:
            if invader_laser.distance(block) <= 20:
                barricade_manager.all_blocks.remove(block)
                invader_manager.all_invader_lasers.remove(invader_laser)
                invader_laser.hideturtle()

                # just for a nice UI experience
                eliminated_list.append(block)
                block.color("LightGreen")
                break

        # if laser hits player
        if invader_laser.distance(player) <= 25:
            player.color("red")
            player.lives -= 1
            invader_manager.all_invader_lasers.remove(invader_laser)
            invader_laser.hideturtle()

        # if laser flies off-screen
        if invader_laser.ycor() <= -500:
            invader_manager.all_invader_lasers.remove(invader_laser)
            invader_laser.hideturtle()

    # check if invaders made it to the base
    for invader in invader_manager.all_invaders:
        if invader.ycor() <= -300:
            player.color("red")
            game_on = False
            break

    # check if player still has lives
    if player.lives == 0:
        game_on = False

    # check if player destroyed all invaders
    if not invader_manager.all_invaders:
        game_on = False


# show final screen
screen.update()

# end program
screen.exitonclick()
