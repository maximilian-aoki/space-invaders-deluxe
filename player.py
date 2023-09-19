from turtle import Turtle

PLAYER_STARTING_POS = (0, -400)


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("square")
        self.color("white")
        self.setposition(PLAYER_STARTING_POS)
        self.setheading(180)

        self.mov_speed = 20

    def move_left(self):
        if self.xcor() >= -420.0:
            self.forward(self.mov_speed)

    def move_right(self):
        if self.xcor() <= 420.0:
            self.backward(self.mov_speed)
