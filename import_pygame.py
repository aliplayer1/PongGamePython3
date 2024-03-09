import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 500, 200
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 30
BALL_SIZE = 10
PADDLE_SPEED = 4
BALL_SPEED = (3.5, 3.5)
SCORE_LIMIT = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Load fonts
font = pygame.font.Font(None, 36)

# Load sounds
paddle_sound = pygame.mixer.Sound("paddle_hit.wav")
wall_sound = pygame.mixer.Sound("wall_hit.wav")
point_sound = pygame.mixer.Sound("point_scored.wav")

# Paddle and ball
paddle_a = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed = list(BALL_SPEED)

# Score
score_a = 0
score_b = 0

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
state = MENU

def reset_game():
    global ball, ball_speed, paddle_a, paddle_b, score_a, score_b
    paddle_a.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    paddle_b.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    ball_speed = list(BALL_SPEED)
    score_a = 0
    score_b = 0

def draw_menu():
    title_text = font.render("PONG", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    instruction_text = font.render("Press SPACE to start", True, WHITE)
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT * 2 // 3))

def draw_game_over(winner):
    game_over_text = font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))

    winner_text = font.render(f"Player {winner} wins!", True, WHITE)
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))

    restart_text = font.render("Press SPACE to restart", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT * 2 // 3))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    if state == MENU:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            state = PLAYING

        draw_menu()

    elif state == PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle_a.top > 0:
            paddle_a.y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle_a.bottom < HEIGHT:
            paddle_a.y += PADDLE_SPEED
        if keys[pygame.K_UP] and paddle_b.top > 0:
            paddle_b.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle_b.bottom < HEIGHT:
            paddle_b.y += PADDLE_SPEED

        # Move ball
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Ball collision with paddles
        if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
            ball_speed[0] = -ball_speed[0]
            paddle_sound.play()

        # Ball collision with walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]
            wall_sound.play()

        # Ball out of bounds
        if ball.left <= 0 or ball.right >= WIDTH:
            if ball.left <= 0:
                score_b += 1
            else:
                score_a += 1
            ball.x = WIDTH // 2 - BALL_SIZE // 2
            ball.y = HEIGHT // 2 - BALL_SIZE // 2
            ball_speed = list(BALL_SPEED)
            point_sound.play()

            if score_a >= SCORE_LIMIT or score_b >= SCORE_LIMIT:
                winner = 1 if score_a >= SCORE_LIMIT else 2
                state = GAME_OVER

        # Draw screen
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle_a)
        pygame.draw.rect(screen, WHITE, paddle_b)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Draw score
        score_text = font.render(f"{score_a} - {score_b}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    elif state == GAME_OVER:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            reset_game()
            state = PLAYING

        draw_game_over(winner)

    pygame.display.flip()
    pygame.time.delay(16)
