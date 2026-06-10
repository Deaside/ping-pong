from pygame import *
from random import choice, randint


WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 60

WHITE = (245, 245, 245)
BLACK = (18, 20, 24)
GRAY = (90, 96, 108)
BLUE = (63, 141, 255)
RED = (255, 92, 92)
YELLOW = (255, 215, 94)

PADDLE_WIDTH = 18
PADDLE_HEIGHT = 105
BALL_SIZE = 20
WIN_SCORE = 5
GOAL_PAUSE_MS = 1200


class GameSprite(sprite.Sprite):
    def __init__(self, color, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = Surface((size_x, size_y))
        self.image.fill(color)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < WIN_HEIGHT - self.rect.height - 5:
            self.rect.y += self.speed

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < WIN_HEIGHT - self.rect.height - 5:
            self.rect.y += self.speed


class Ball(GameSprite):
    def __init__(self):
        super().__init__(YELLOW, WIN_WIDTH // 2 - BALL_SIZE // 2, WIN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE, 0)
        self.speed_x = 5
        self.speed_y = 4

    def reset(self, direction):
        self.rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
        self.speed_x = direction * 5
        self.speed_y = choice([-4, -3, 3, 4])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= WIN_HEIGHT:
            self.speed_y *= -1


def draw_text(window, text, size, color, x, y):
    label_font = font.Font(None, size)
    label = label_font.render(text, True, color)
    label_rect = label.get_rect(center=(x, y))
    window.blit(label, label_rect)


def draw_center_line(window):
    for y in range(0, WIN_HEIGHT, 34):
        draw.rect(window, GRAY, (WIN_WIDTH // 2 - 3, y, 6, 18))


display.init()
font.init()

display.set_caption("Ping Pong 2D")
window = display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = time.Clock()

left_player = Player(BLUE, 25, WIN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, 7)
right_player = Player(RED, WIN_WIDTH - 25 - PADDLE_WIDTH, WIN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, 7)
ball = Ball()
ball.reset(choice([-1, 1]))

left_score = 0
right_score = 0
game_over = False
winner_text = ""
goal_text = ""
goal_pause_until = 0
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and e.key == K_SPACE and game_over:
            left_score = 0
            right_score = 0
            game_over = False
            winner_text = ""
            goal_text = ""
            goal_pause_until = 0
            left_player.rect.y = WIN_HEIGHT // 2 - PADDLE_HEIGHT // 2
            right_player.rect.y = WIN_HEIGHT // 2 - PADDLE_HEIGHT // 2
            ball.reset(choice([-1, 1]))

    now = time.get_ticks()
    goal_pause = now < goal_pause_until

    if not game_over and not goal_pause:
        left_player.update_l()
        right_player.update_r()
        ball.update()

        if sprite.collide_rect(ball, left_player) and ball.speed_x < 0:
            ball.speed_x *= -1
            ball.speed_y += randint(-1, 1)
            ball.rect.left = left_player.rect.right

        if sprite.collide_rect(ball, right_player) and ball.speed_x > 0:
            ball.speed_x *= -1
            ball.speed_y += randint(-1, 1)
            ball.rect.right = right_player.rect.left

        if ball.rect.right < 0:
            right_score += 1
            goal_text = "Правый игрок забил!"
            goal_pause_until = time.get_ticks() + GOAL_PAUSE_MS
            ball.reset(1)

        if ball.rect.left > WIN_WIDTH:
            left_score += 1
            goal_text = "Левый игрок забил!"
            goal_pause_until = time.get_ticks() + GOAL_PAUSE_MS
            ball.reset(-1)

        if left_score >= WIN_SCORE:
            game_over = True
            winner_text = "Победил левый игрок!"

        if right_score >= WIN_SCORE:
            game_over = True
            winner_text = "Победил правый игрок!"

    window.fill(BLACK)
    draw_center_line(window)

    window.blit(left_player.image, left_player.rect)
    window.blit(right_player.image, right_player.rect)
    draw.ellipse(window, YELLOW, ball.rect)

    draw_text(window, str(left_score), 74, WHITE, WIN_WIDTH // 2 - 75, 55)
    draw_text(window, str(right_score), 74, WHITE, WIN_WIDTH // 2 + 75, 55)
    draw_text(window, "W/S", 28, BLUE, 60, 28)
    draw_text(window, "↑/↓", 28, RED, WIN_WIDTH - 60, 28)

    if game_over:
        draw_text(window, winner_text, 54, WHITE, WIN_WIDTH // 2, WIN_HEIGHT // 2 - 24)
        draw_text(window, "Нажми SPACE, чтобы начать заново", 32, WHITE, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 28)
    elif goal_pause:
        draw_text(window, goal_text, 48, WHITE, WIN_WIDTH // 2, WIN_HEIGHT // 2)

    display.update()
    clock.tick(FPS)

quit()
