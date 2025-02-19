import pygame


pygame.init()

WIDTH = 800
HEIGHT = 600
BALL_SPEED = 5
PADDLE_SPEED = 7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pong Game")

ball = pygame.Rect(WIDTH//2-10, HEIGHT//2-10, 20, 20)
player_paddle = pygame.Rect(WIDTH - 20, HEIGHT//2-50, 10, 100)
opponent_paddle = pygame.Rect(10, HEIGHT//2-50, 10, 100)

ball_dx, ball_dy = BALL_SPEED, BALL_SPEED






running = True

while running:
    pygame.time.delay(16)
    screen.fill(BLACK)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        player_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP]:
        player_paddle.y -= PADDLE_SPEED

    
    ball.x += ball_dx
    ball.y += ball_dy

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_dx *= -1

    if ball.left <= 0 or ball.right >= WIDTH:
        ball.x, ball.y = WIDTH//2 - 10, HEIGHT//2 - 10
        ball_dx, ball_dy = BALL_SPEED, BALL_SPEED
        player_paddle.y = HEIGHT//2 - 50
        opponent_paddle.y = HEIGHT//2 - 50



    if player_paddle.top <= 0:
        player_paddle.top = 0


    if player_paddle.bottom >= HEIGHT:
        player_paddle.bottom = HEIGHT


    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    pygame.display.flip()




pygame.quit()