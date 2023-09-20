from turtle import Turtle


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.setposition(-500, -465)

        self.score = 0
        self.write(arg=f"SCORE: {self.score}", align="left", font=("Courier", 24, "normal"))

    def hit_score(self, invader_difficulty):
        self.clear()
        if invader_difficulty == "easy":
            self.score += 10
        elif invader_difficulty == "medium":
            self.score += 25
        elif invader_difficulty == "hard":
            self.score += 50
        self.write(arg=f"SCORE: {self.score}", align="left", font=("Courier", 24, "normal"))

    def mystery_score(self):
        self.clear()
        self.score += 300
        self.write(arg=f"SCORE: {self.score}", align="left", font=("Courier", 24, "normal"))


class HealthBar(Turtle):
    def __init__(self, player):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.setposition(-300, -465)

        self.lives = player.lives
        self.write(arg=f"HEALTH: {' '.join(self.lives)}", align="left", font=("Courier", 24, "normal"))

    def player_hit(self, scoreboard):
        self.clear()
        self.lives.remove(self.lives[-1])
        self.write(arg=f"HEALTH: {' '.join(self.lives)}", align="left", font=("Courier", 24, "normal"))
        scoreboard.clear()
        scoreboard.score -= 200
        if scoreboard.score < 0:
            scoreboard.score = 0
        scoreboard.write(arg=f"SCORE: {scoreboard.score}", align="left", font=("Courier", 24, "normal"))


class Title(Turtle):
    def __init__(self, message_str):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.setposition(0, 400)
        self.write(arg=message_str, align="center", font=("Courier", 60, "bold"))


class Info(Turtle):
    def __init__(self, message_str):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.setposition(-475, 475)
        self.write(arg=message_str, align="center", font=("Courier", 18, "normal"))