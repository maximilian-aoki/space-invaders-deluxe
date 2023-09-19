from turtle import Turtle, Screen
from player import Player
import time

# initialize turtle Screen instance
screen = Screen()
screen.bgcolor("black")
screen.setup(width=1000, height=1000)
screen.tracer(0)

# initialize gameplay objects
player = Player()

# listen for player key presses
screen.listen()
screen.onkey(fun=player.move_left, key="Left")
screen.onkey(fun=player.move_right, key="Right")
screen.onkey(fun=player.shoot, key="space")

# gameplay
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
