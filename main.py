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

# gameplay
game_on = True
while game_on:
    time.sleep(0.1)
    screen.update()


# end program
screen.exitonclick()
