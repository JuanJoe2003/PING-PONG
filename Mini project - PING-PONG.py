import pygame
import random

# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PING-PONG")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont('Consolas', 30)

    # Paddles and Ball
    paddle_1_rect = pygame.Rect(30, 0, 7, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, 0, 7, 100)
    ball_rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 25, 25)

    # Movement values
    paddle_1_move = 0
    paddle_2_move = 0

    ball_accel_x = random.randint(2, 4) * 0.1
    ball_accel_y = random.randint(2, 4) * 0.1
    if random.randint(1, 2) == 1:
        ball_accel_x *= -1
    if random.randint(1, 2) == 1:
        ball_accel_y *= -1

    started = False

    running = True
    while running:
        delta_time = clock.tick(60)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    started = True
                if event.key == pygame.K_w:
                    paddle_1_move = -0.5
                if event.key == pygame.K_s:
                    paddle_1_move = 0.5
                if event.key == pygame.K_UP:
                    paddle_2_move = -0.5
                if event.key == pygame.K_DOWN:
                    paddle_2_move = 0.5

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    paddle_1_move = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    paddle_2_move = 0

        # Game Logic
        if started:
            ball_rect.left += ball_accel_x * delta_time
            ball_rect.top += ball_accel_y * delta_time

        paddle_1_rect.top += paddle_1_move * delta_time
        paddle_2_rect.top += paddle_2_move * delta_time

        # Prevent paddles from going out of bounds
        paddle_1_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        paddle_2_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Wall collisions
        if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
            ball_accel_y *= -1

        # Left or right wall = Game over or restart logic
        if ball_rect.left <= 0 or ball_rect.right >= SCREEN_WIDTH:
            started = False
            ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Paddle collisions
        if paddle_1_rect.colliderect(ball_rect) and ball_accel_x < 0:
            ball_accel_x *= -1
            ball_rect.left = paddle_1_rect.right

        if paddle_2_rect.colliderect(ball_rect) and ball_accel_x > 0:
            ball_accel_x *= -1
            ball_rect.right = paddle_2_rect.left

        # Drawing
        screen.fill(COLOR_BLUE)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)
        pygame.draw.rect(screen, COLOR_WHITE, ball_rect)

        if not started:
            text = font.render('Press Space to Start', True, COLOR_WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
