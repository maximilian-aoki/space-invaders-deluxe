from turtle import Screen
from player import Player
from invader_manager import InvaderManager
from barricade_manager import BarricadeManager
from gameboard import Score, HealthBar, Title, Subtitle, Info
import upgrades
from datetime import datetime
import time

# ------------------------- INITIALIZE GAME OBJECTS ------------------------- #

# initialize turtle Screen instance
screen = Screen()
screen.bgcolor("black")
screen.setup(width=1200, height=1000)
screen.tracer(0)

# artificial timer
start_time = datetime.now()

# initialize gameplay objects
player = Player()
invader_manager = InvaderManager()
barricade_manager = BarricadeManager()

score = Score()
health_bar = HealthBar(player=player)
info = Info(message_str="click screen to exit")

# listen for player key presses
screen.listen()
screen.onkeypress(fun=player.move_left, key="Left")
screen.onkeypress(fun=player.move_right, key="Right")
screen.onkeypress(fun=player.shoot, key="space")


# initialize all invaders
invader_manager.create_invaders()
eliminated_list = []

# --------------------------- GAMEPLAY --------------------------- #

game_on = True
round_win = False
while game_on:
    # update the player's screen
    screen.update()
    time.sleep(0.1)

    # reset colors and eliminated objects after hits
    player.color("white")
    for item in eliminated_list:
        eliminated_list.remove(item)
        item.hideturtle()

    # --------------------------- MOVE TURNS --------------------------- #

    # player lasers move
    for laser in player.all_lasers:
        laser.forward(player.laser_speed)

    # invaders move and shoot turn (based on asynchronous invader timer)
    time_check = (datetime.now() - start_time).total_seconds()
    if time_check >= invader_manager.move_time:
        invader_manager.invaders_turn()
        start_time = datetime.now()

    # move all invader's lasers
    for invader_laser in invader_manager.all_invader_lasers:
        invader_laser.forward(invader_laser.laser_speed)

    # --------------------------- PLAYER LASER CONDITIONALS --------------------------- #

    # if player laser hits invader
    for laser in player.all_lasers:
        for invader in invader_manager.all_invaders:
            if laser.distance(invader) <= 23:
                invader_manager.all_invaders.remove(invader)
                player.all_lasers.remove(laser)
                laser.hideturtle()

                # just for a nice UI experience
                eliminated_list.append(invader)
                invader.color("LightGreen")
                score.hit_score(invader.difficulty)

                # make it slightly more likely that each invader will shoot
                invader_manager.laser_factor -= 1
                break
        if invader_manager.mystery_ship:
            if laser.distance(invader_manager.mystery_ship[0]) <= 23:
                player.all_lasers.remove(laser)
                laser.hideturtle()

                eliminated_list.append(invader_manager.mystery_ship[0])
                invader_manager.mystery_ship[0].color("LightGreen")
                invader_manager.mystery_ship.remove(invader_manager.mystery_ship[0])

                score.mystery_score()

    # if player laser hits barricade
    for laser in player.all_lasers:
        for block in barricade_manager.all_blocks:
            if laser.distance(block) <= 21:
                barricade_manager.all_blocks.remove(block)
                player.all_lasers.remove(laser)
                laser.hideturtle()

                # just for a nice UI experience
                eliminated_list.append(block)
                block.color("LightGreen")
                break

    # if player laser flies off-screen
    for laser in player.all_lasers:
        if laser.ycor() >= 500:
            player.all_lasers.remove(laser)
            laser.hideturtle()

    # if player laser collides with invader laser
    for laser in player.all_lasers:
        for invader_laser in invader_manager.all_invader_lasers:
            if (laser.xcor() >= invader_laser.xcor() - 1) and (laser.xcor() <= invader_laser.xcor() + 1):
                if laser.ycor() >= invader_laser.ycor():
                    player.all_lasers.remove(laser)
                    invader_manager.all_invader_lasers.remove(invader_laser)
                    laser.hideturtle()
                    invader_laser.hideturtle()
                    break

    # --------------------------- INVADER LASER CONDITIONALS --------------------------- #

    # if invader laser hits barricade
    for invader_laser in invader_manager.all_invader_lasers:
        for block in barricade_manager.all_blocks:
            if invader_laser.distance(block) <= 21:
                barricade_manager.all_blocks.remove(block)
                invader_manager.all_invader_lasers.remove(invader_laser)
                invader_laser.hideturtle()

                # just for a nice UI experience
                eliminated_list.append(block)
                block.color("LightGreen")
                break

    # if invader laser hits player
    for invader_laser in invader_manager.all_invader_lasers:
        if invader_laser.distance(player) <= 25:
            player.color("red")
            health_bar.player_hit(scoreboard=score)
            invader_manager.all_invader_lasers.remove(invader_laser)
            invader_laser.hideturtle()

            break

    # if invader laser flies off-screen
    for invader_laser in invader_manager.all_invader_lasers:
        if invader_laser.ycor() <= -500:
            invader_manager.all_invader_lasers.remove(invader_laser)
            invader_laser.hideturtle()

    # --------------------------- ENDGAME CONDITIONALS --------------------------- #

    # check if invaders made it to the base
    for invader in invader_manager.all_invaders:
        if invader.ycor() <= -300:
            player.color("red")
            game_on = False
            break

    # check if player lost all lives
    if not player.lives:
        game_on = False

    # check if player destroyed all invaders (ONLY WIN CONDITION)
    if not invader_manager.all_invaders:
        game_on = False
        round_win = True

        win_title = Title(message_str="ROUND WIN")
        win_subtitle = Subtitle(message_str="See console output for player upgrades :)")

        upgrades.upgrade_menu(score_board=score.score)


# show final screen on loss
game_over = Title(message_str="GAME OVER")
game_over_subtitle = Subtitle(message_str="Better luck next time!")
screen.update()

# end program
screen.exitonclick()
