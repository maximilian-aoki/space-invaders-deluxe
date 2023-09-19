from turtle import Turtle
import random


class InvaderManager(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.all_invaders = []
        self.start_ycor = 50.0

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
