from turtle import Turtle

PLAYER_STARTING_POS = (0, -400)


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=2, stretch_len=3)
        self.color("white")
        self.setposition(PLAYER_STARTING_POS)
        self.setheading(180)

        self.mov_speed = 20
        self.all_lasers = []
        self.laser_speed = 30
        self.lives = ["♥", "♥", "♥"]

    def move_left(self):
        if self.xcor() >= -520.0:
            self.forward(self.mov_speed)

    def move_right(self):
        if self.xcor() <= 520.0:
            self.backward(self.mov_speed)

    def shoot(self):
        if len(self.all_lasers) == 0 or self.all_lasers[-1].ycor() >= -100.0:
            self.all_lasers.append(PlayerLaser(self))


class PlayerLaser(Turtle):
    def __init__(self, player):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=0.2, stretch_len=1)
        self.color("white")
        self.setheading(90)
        self.setposition(player.position())
