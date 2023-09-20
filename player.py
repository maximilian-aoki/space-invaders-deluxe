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
        self.fire_rate = -100
        self.lives = ["♥", "♥", "♥"]

        self.device_status = True
        self.device = []
        self.device_speed = 10

    def move_left(self):
        if self.xcor() >= -520.0:
            self.forward(self.mov_speed)

    def move_right(self):
        if self.xcor() <= 520.0:
            self.backward(self.mov_speed)

    def shoot(self):
        if len(self.all_lasers) == 0 or self.all_lasers[-1].ycor() >= self.fire_rate:
            self.all_lasers.append(PlayerLaser(self))

    def drop_device(self):
        if self.device_status:
            print("The INVADERS won't like this one...\n")
            self.device_status = False
            self.device.append(PlayerDevice(self))


class PlayerLaser(Turtle):
    def __init__(self, player):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=0.2, stretch_len=1)
        self.color("white")
        self.setheading(90)
        self.setposition(player.position())


class PlayerDevice(Turtle):
    def __init__(self, player):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=0.2, stretch_len=0.2)
        self.color("LightGreen")
        self.setheading(90)
        self.setposition(player.position())


class DeviceExplosion(Turtle):
    def __init__(self, device):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.shapesize(stretch_wid=28, stretch_len=28)
        self.color("LightGreen")
        self.setposition(device.position())

