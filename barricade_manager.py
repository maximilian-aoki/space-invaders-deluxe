from turtle import Turtle

BARRICADE_NODES_Y = -300

BARRICADE_NODES_X = [-450, -300, -150, 0, 150, 300, 450]
BARRICADE_COLS = [-50, -25, 0, 25, 50]
BARRICADE_ROWS = [0, -25]


class BarricadeManager:
    def __init__(self):
        self.all_blocks = []

        for i in BARRICADE_NODES_X:
            for j in BARRICADE_COLS:
                for k in BARRICADE_ROWS:
                    self.all_blocks.append(Barricade(position=(i + j, BARRICADE_NODES_Y + k)))


class Barricade(Turtle):
    def __init__(self, position):
        super().__init__()
        self.penup()
        self.color("grey")
        self.shape("square")
        self.setposition(position)
