from turtle import Screen
from player import Player, DeviceExplosion
from invader_manager import InvaderManager
from barricade_manager import BarricadeManager
from gameboard import Score, HealthBar, DeviceBar, Title, Subtitle, Info
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

# initialize round modifier
round_mod = 1

# initialize gameplay objects
player = Player()
invader_manager = InvaderManager()
barricade_manager = BarricadeManager()

score = Score(round=round_mod, score=1000)
health_bar = HealthBar(player=player)
device_bar = DeviceBar(player=player)
info = Info(message_str="hit [esc] to end game")


# listen for player key presses
screen.listen()
screen.onkeypress(fun=player.move_left, key="Left")
screen.onkeypress(fun=player.move_right, key="Right")
screen.onkeypress(fun=player.shoot, key="space")
screen.onkeypress(fun=player.drop_device, key="Return")


def quit_program():
    Title(message_str="GAME OVER")
    Subtitle(message_str="Click screen to exit")
    screen.update()
    screen.exitonclick()
    screen.bye()


screen.onkeypress(fun=quit_program, key="Escape")

# initialize all invaders
invader_manager.create_invaders()
eliminated_list = []

# --------------------------- GAMEPLAY --------------------------- #

game_on = True
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

    # player lasers move (if applicable)
    for laser in player.all_lasers:
        laser.forward(player.laser_speed)

    # player device move (if applicable)
    for device in player.device:
        device_bar.update_device_status(player=player)
        device.forward(player.device_speed)
        if device.ycor() >= 500:
            player.device.remove(device)
            device.hideturtle()

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

                score.hit_score(invader_manager.mystery_ship[0].difficulty)
                invader_manager.mystery_ship.remove(invader_manager.mystery_ship[0])

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

    # if player device collides with any invader
    for device in player.device:
        all_invaders = invader_manager.all_invaders + invader_manager.mystery_ship
        for invader_pass1 in all_invaders:
            if device.distance(invader_pass1) <= 23:
                explosion = DeviceExplosion(device=device)
                for invader_pass2 in all_invaders:
                    if explosion.distance(invader_pass2) <= 300:
                        if invader_pass2 in invader_manager.all_invaders:
                            invader_manager.all_invaders.remove(invader_pass2)
                        elif invader_pass2 in invader_manager.mystery_ship:
                            invader_manager.mystery_ship.remove(invader_pass2)
                        invader_pass2.color("LightGreen")
                        eliminated_list.append(invader_pass2)
                        score.hit_score(invader_pass2.difficulty)

                        # make it slightly more likely that each invader will shoot
                        invader_manager.laser_factor -= 1

                player.device_status = False
                player.device.remove(device)
                # just for a nice UI experience
                eliminated_list.append(device)
                eliminated_list.append(explosion)
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
        game_on = True
        win_title = Title(message_str="ROUND WIN")
        win_subtitle = Subtitle(message_str="See console output for player upgrades :)")
        screen.update()

        round_mod += 1

        # take player to upgrade menu and reset screen on completion
        upgraded_items = upgrades.upgrade_menu(score_board=score.score)
        screen.reset()

        # --------------------- RESET ALL OBJECTS AND BINDS / INCLUDE UPGRADES --------------------- #

        score = Score(round=round_mod, score=upgraded_items["score"])

        player = Player()
        for armor in upgraded_items["armor"]:
            player.lives.append(armor)
        if upgraded_items["fire_rate"]:
            player.fire_rate = upgraded_items["fire_rate"]
        if upgraded_items["device"]:
            player.device_status = True

        barricade_manager = BarricadeManager()

        # add difficulty increases
        invader_manager = InvaderManager()
        invader_manager.start_ycor -= 20 * (round_mod - 1)
        invader_manager.move_time -= 0.1 * (round_mod - 1)
        invader_manager.laser_factor -= 2 * (round_mod - 1)

        health_bar = HealthBar(player=player)
        device_bar = DeviceBar(player=player)
        info = Info(message_str="hit [esc] to end game")

        # listen for player key presses
        screen.listen()
        screen.onkeypress(fun=player.move_left, key="Left")
        screen.onkeypress(fun=player.move_right, key="Right")
        screen.onkeypress(fun=player.shoot, key="space")
        screen.onkeypress(fun=player.drop_device, key="Return")


        def quit_program():
            Title(message_str="GAME OVER")
            Subtitle(message_str="Click screen to exit")
            screen.update()
            screen.exitonclick()
            screen.bye()


        screen.onkeypress(fun=quit_program, key="Escape")

        # initialize all invaders
        invader_manager.create_invaders()
        eliminated_list = []


# show final screen on loss
game_over = Title(message_str="GAME OVER")
game_over_subtitle = Subtitle(message_str="Click screen to exit")
screen.update()

# end program
screen.exitonclick()
