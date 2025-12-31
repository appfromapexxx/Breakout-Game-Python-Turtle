"""
Breakout Game - 使用 Python Turtle 製作的經典打磚塊遊戲
"""

from turtle import Turtle, Screen
from random import choice

# =============================================================================
# 遊戲配置常數
# =============================================================================

# 視窗設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = "black"

# 擋板設定
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 1
PADDLE_COLOR = "white"
PADDLE_Y = -250
PADDLE_SPEED = 40

# 球設定
BALL_COLOR = "white"
BALL_SHAPE = "circle"
BALL_X_SPEED = 4
BALL_Y_SPEED = 4

# 磚塊設定
BRICK_COLORS = [
    "red", "orange", "yellow", "green", "cyan",
    "blue", "purple", "pink", "gold", "white"
]
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 3
BRICK_HEIGHT = 1
BRICK_START_X = -350
BRICK_START_Y = 250
BRICK_SPACING_X = 78
BRICK_SPACING_Y = 30

# 遊戲設定
INITIAL_LIVES = 3
POINTS_PER_BRICK = 10

# =============================================================================
# 遊戲類別
# =============================================================================


class Paddle(Turtle):
    """玩家控制的擋板"""

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(PADDLE_HEIGHT, PADDLE_WIDTH)
        self.color(PADDLE_COLOR)
        self.penup()
        self.goto(0, PADDLE_Y)

    def move_left(self):
        """向左移動擋板"""
        new_x = self.xcor() - PADDLE_SPEED
        if new_x > -SCREEN_WIDTH / 2 + 50:
            self.goto(new_x, self.ycor())

    def move_right(self):
        """向右移動擋板"""
        new_x = self.xcor() + PADDLE_SPEED
        if new_x < SCREEN_WIDTH / 2 - 50:
            self.goto(new_x, self.ycor())


class Ball(Turtle):
    """遊戲中的球"""

    def __init__(self):
        super().__init__()
        self.shape(BALL_SHAPE)
        self.color(BALL_COLOR)
        self.penup()
        self.x_speed = BALL_X_SPEED
        self.y_speed = -BALL_Y_SPEED  # 初始向下移動

    def move(self):
        """移動球"""
        new_x = self.xcor() + self.x_speed
        new_y = self.ycor() + self.y_speed
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Y 軸反彈"""
        self.y_speed *= -1

    def bounce_x(self):
        """X 軸反彈"""
        self.x_speed *= -1

    def reset(self):
        """重置球的位置"""
        self.goto(0, 0)
        self.y_speed = -abs(self.y_speed)  # 確保向下移動


class Brick(Turtle):
    """可被擊破的磚塊"""

    def __init__(self, x: int, y: int, color: str):
        super().__init__()
        self.shape("square")
        self.shapesize(BRICK_HEIGHT, BRICK_WIDTH)
        self.color(color)
        self.penup()
        self.goto(x, y)


class Scoreboard(Turtle):
    """計分板"""

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("white")
        self.goto(0, SCREEN_HEIGHT / 2 - 40)
        self.score = 0
        self.lives = INITIAL_LIVES
        self.update_display()

    def update_display(self):
        """更新顯示"""
        self.clear()
        self.write(
            f"分數: {self.score}  |  生命: {'❤️' * self.lives}",
            align="center",
            font=("Arial", 16, "bold")
        )

    def add_score(self, points: int = POINTS_PER_BRICK):
        """增加分數"""
        self.score += points
        self.update_display()

    def lose_life(self) -> bool:
        """失去一條生命，回傳是否還有生命"""
        self.lives -= 1
        self.update_display()
        return self.lives > 0

    def show_game_over(self):
        """顯示遊戲結束"""
        self.goto(0, 0)
        self.write(
            "遊戲結束！",
            align="center",
            font=("Arial", 36, "bold")
        )

    def show_victory(self):
        """顯示勝利"""
        self.goto(0, 0)
        self.write(
            f"恭喜過關！總分: {self.score}",
            align="center",
            font=("Arial", 36, "bold")
        )

    def show_restart_hint(self):
        """顯示重新開始提示"""
        self.goto(0, -50)
        self.write(
            "按 R 鍵重新開始",
            align="center",
            font=("Arial", 18, "normal")
        )


# =============================================================================
# 遊戲主程式
# =============================================================================


def create_bricks() -> list[Brick]:
    """建立所有磚塊"""
    bricks = []
    for row in range(BRICK_ROWS):
        color = BRICK_COLORS[row % len(BRICK_COLORS)]
        for col in range(BRICK_COLS):
            x = BRICK_START_X + col * BRICK_SPACING_X
            y = BRICK_START_Y - row * BRICK_SPACING_Y
            brick = Brick(x, y, color)
            bricks.append(brick)
    return bricks


def check_brick_collision(ball: Ball, bricks: list[Brick], scoreboard: Scoreboard) -> bool:
    """檢查球與磚塊的碰撞，回傳是否發生碰撞"""
    for brick in bricks[:]:  # 使用切片複製列表以避免在迭代中修改
        if ball.distance(brick) < 35:
            ball.bounce_y()
            brick.hideturtle()
            bricks.remove(brick)
            scoreboard.add_score()
            return True
    return False


def main():
    """遊戲主程式"""
    # 設定螢幕
    screen = Screen()
    screen.title("Breakout Game - 打磚塊遊戲")
    screen.bgcolor(BG_COLOR)
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.tracer(0)

    # 遊戲狀態
    game_state = {"restart_requested": False}

    def request_restart():
        """請求重新開始遊戲"""
        game_state["restart_requested"] = True

    def clear_all_objects(objects_list: list):
        """隱藏並清除所有物件"""
        for obj in objects_list:
            obj.hideturtle()
        objects_list.clear()

    def run_game():
        """執行一輪遊戲"""
        # 重置狀態
        game_state["restart_requested"] = False

        # 建立遊戲物件
        paddle = Paddle()
        ball = Ball()
        scoreboard = Scoreboard()
        bricks = create_bricks()

        # 所有物件列表（用於清理）
        all_objects = [paddle, ball, scoreboard] + bricks[:]

        # 設定鍵盤控制
        screen.listen()
        screen.onkey(paddle.move_left, "Left")
        screen.onkey(paddle.move_right, "Right")
        screen.onkey(paddle.move_left, "a")
        screen.onkey(paddle.move_right, "d")
        screen.onkey(request_restart, "r")
        screen.onkey(request_restart, "R")

        # 遊戲主迴圈
        game_is_on = True

        while game_is_on:
            screen.update()
            ball.move()

            # 檢查重新開始請求
            if game_state["restart_requested"]:
                clear_all_objects(all_objects)
                return True  # 回傳 True 表示要重新開始

            # 檢查牆壁碰撞
            if ball.xcor() > SCREEN_WIDTH / 2 - 10 or ball.xcor() < -SCREEN_WIDTH / 2 + 10:
                ball.bounce_x()

            # 檢查頂部碰撞
            if ball.ycor() > SCREEN_HEIGHT / 2 - 10:
                ball.bounce_y()

            # 檢查擋板碰撞
            if ball.distance(paddle) < 60 and ball.ycor() < PADDLE_Y + 20:
                ball.bounce_y()

            # 檢查磚塊碰撞
            check_brick_collision(ball, bricks, scoreboard)

            # 檢查勝利條件
            if len(bricks) == 0:
                scoreboard.show_victory()
                scoreboard.show_restart_hint()
                game_is_on = False

            # 檢查球落地
            if ball.ycor() < -SCREEN_HEIGHT / 2:
                if scoreboard.lose_life():
                    ball.reset()
                else:
                    scoreboard.show_game_over()
                    scoreboard.show_restart_hint()
                    game_is_on = False

        # 等待重新開始
        while not game_state["restart_requested"]:
            screen.update()

        clear_all_objects(all_objects)
        return True

    # 主遊戲迴圈
    while run_game():
        pass

    screen.mainloop()


if __name__ == "__main__":
    main()