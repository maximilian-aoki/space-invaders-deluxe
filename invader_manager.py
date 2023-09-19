from turtle import Turtle
import random


class InvaderManager:
    def __init__(self):
        self.all_invaders = []
        self.all_invader_lasers = []

        # movement characteristics
        self.start_ycor = 150
        self.orientation = 0
        self.move_speed = 20.0
        self.move_time = 1.0

        # attack characteristics
        self.laser_factor = 50

    def create_invaders(self):
        for row_level in ["easy", "easy", "medium", "medium", "hard"]:
            self.all_invaders.append(
                Invader(difficulty=row_level, position=(0.0, self.start_ycor))
            )
            for i in range(1, 5):
                for j in [-i, i]:
                    self.all_invaders.append(
                        Invader(difficulty=row_level, position=(j * 60, self.start_ycor))
                    )
            self.start_ycor += 60

    def invaders_turn(self):
        # movement phase
        at_edge = False
        for invader in self.all_invaders:
            if (invader.xcor() == 540 and self.orientation == 0) \
                    or (invader.xcor() == -540 and self.orientation == 180):
                if invader.xcor() == 540:
                    self.orientation = 180
                elif invader.xcor() == -540:
                    self.orientation = 0
                at_edge = True
                break
        if at_edge:
            for invader in self.all_invaders:
                invader.setposition((invader.xcor(), invader.ycor() - 60))
                invader.setheading(self.orientation)
            self.move_time -= 0.1
        elif not at_edge:
            for invader in self.all_invaders:
                invader.forward(self.move_speed)

        # attack phase
        for invader in self.all_invaders:
            die_roll = random.randint(1, self.laser_factor)
            if die_roll == 1:
                self.all_invader_lasers.append(InvaderLaser(invader=invader))
                break


class Invader(Turtle):
    def __init__(self, difficulty, position):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.setheading(0)

        self.difficulty = difficulty
        self.setposition(position)

        if self.difficulty == "easy":
            self.color("PaleTurquoise1")
        elif self.difficulty == "medium":
            self.color("khaki1")
        elif self.difficulty == "hard":
            self.color("coral1")


class InvaderLaser(Turtle):
    def __init__(self, invader):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=0.2, stretch_len=1)
        self.setheading(270)

        self.setposition(invader.position())
        self.difficulty = invader.difficulty

        if self.difficulty == "easy":
            self.color("PaleTurquoise1")
            self.laser_speed = 20
        elif self.difficulty == "medium":
            self.color("khaki1")
            self.laser_speed = 30
        elif self.difficulty == "hard":
            self.color("coral1")
            self.laser_speed = 40
