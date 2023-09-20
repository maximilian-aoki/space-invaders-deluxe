from turtle import Turtle


class Score(Turtle):
    def __init__(self, round, score):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.setposition(-575, -465)

        self.round = round
        self.score = score
        self.write(arg=f"ROUND: {self.round}  CREDITS: {self.score}", align="left", font=("Courier", 24, "normal"))

    def hit_score(self, invader_difficulty):
        self.clear()
        if invader_difficulty == "easy":
            self.score += 10
        elif invader_difficulty == "medium":
            self.score += 25
        elif invader_difficulty == "hard":
            self.score += 50
        elif invader_difficulty == "mystery":
            self.score += 300
        self.write(arg=f"ROUND: {self.round}  CREDITS: {self.score}", align="left", font=("Courier", 24, "normal"))


class HealthBar(Turtle):
    def __init__(self, player):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.setposition(-200, -465)

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
        scoreboard.write(
            arg=f"ROUND: {scoreboard.round}  CREDITS: {scoreboard.score}",
            align="left",
            font=("Courier", 24, "normal")
        )


class DeviceBar(Turtle):
    def __init__(self, player):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.setposition(200, -465)

        self.status = player.device_status
        if self.status:
            self.color("LightGreen")
            self.write(arg=f"Device: ARMED [hit return]",
                       align="left",
                       font=("Courier", 24, "normal"))
        else:
            self.color("white")
            self.write(arg=f"Device: None",
                       align="left",
                       font=("Courier", 24, "normal"))

    def update_device_status(self, player):
        self.clear()
        self.status = player.device_status
        if self.status:
            self.color("LightGreen")
            self.write(arg="Device: ARMED [hit return]",
                       align="left",
                       font=("Courier", 24, "normal"))
        else:
            self.color("white")
            self.write(arg="Device: None",
                       align="left",
                       font=("Courier", 24, "normal"))


class Title(Turtle):
    def __init__(self, message_str):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.setposition(0, 420)
        self.write(arg=message_str, align="center", font=("Courier", 60, "bold"))


class Subtitle(Turtle):
    def __init__(self, message_str):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.setposition(0, 400)
        self.write(arg=message_str, align="center", font=("Courier", 24, "normal"))


class Info(Turtle):
    def __init__(self, message_str):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.setposition(-450, 435)
        self.write(arg=message_str, align="center", font=("Courier", 18, "normal"))