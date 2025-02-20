import pygame
import random


pygame.init()

difficulty =  "N"   #input("With what difficulty would you want to play with? {E} easy, {N} normal, {H} hard: ")

if difficulty.upper() == "E":
    BALL_SPEED = 3
    PADDLE_SPEED = 5
elif difficulty.upper() == "N":
    BALL_SPEED = 5
    PADDLE_SPEED = 7
elif difficulty.upper() == "H":
    BALL_SPEED = 7
    PADDLE_SPEED = 9
else:
    BALL_SPEED = 5
    PADDLE_SPEED = 7

first_run = True

WIDTH = 800
HEIGHT = 600


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

own_score = 0
opponent_score = 0

font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pong Game")

ball = pygame.Rect((WIDTH//2-10), random.randint(0, HEIGHT-20), 20, 20)
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

    
    if first_run:

        countdown_font = pygame.font.Font(None, 60)

        countdown = countdown_font.render("3", True, WHITE)
        screen.blit(countdown, (WIDTH//2-countdown.get_width()//2, HEIGHT//2-countdown.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(1000)
        screen.fill(BLACK)

        countdown = countdown_font.render("2", True, WHITE)
        screen.blit(countdown, (WIDTH//2-countdown.get_width()//2, HEIGHT//2-countdown.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(1000)
        screen.fill(BLACK)

        countdown = countdown_font.render("1", True, WHITE)
        screen.blit(countdown, (WIDTH//2-countdown.get_width()//2, HEIGHT//2-countdown.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(1000)
        screen.fill(BLACK)

        countdown = countdown_font.render("", True, WHITE)
        screen.blit(countdown, (WIDTH//2-countdown.get_width()//2, HEIGHT//2-countdown.get_height()//2))
        pygame.display.flip()

        
        first_run = False


    ball.x += ball_dx
    ball.y += ball_dy

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_dx *= -1

        # Ändert die Flugbahn basierend auf der Position des Schlägers
        if keys[pygame.K_DOWN]:
            ball_dy += 0.5
        if keys[pygame.K_UP]:
            ball_dy -= 0.5
        if opponent_paddle.centery < ball.centery:
            ball_dy += 0.5
        if opponent_paddle.centery > ball.centery:
            ball_dy -= 0.5

    if ball.left <= 0:
        ball.x, ball.y = WIDTH//2 - 10, random.randint(0, HEIGHT-20)
        ball_dx, ball_dy = random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])
        player_paddle.y = HEIGHT//2 - 50
        opponent_paddle.y = HEIGHT//2 - 50

        own_score += 1

    if ball.right >= WIDTH:
        ball.x, ball.y = WIDTH//2 - 10, random.randint(0, HEIGHT-20)
        ball_dx, ball_dy = random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])
        player_paddle.y = HEIGHT//2 - 50
        opponent_paddle.y = HEIGHT//2 - 50

        opponent_score += 1



    
    if opponent_paddle.y < ball.y:
        opponent_paddle.y += PADDLE_SPEED
    elif opponent_paddle.y > ball.y:
        opponent_paddle.y -= PADDLE_SPEED






    if player_paddle.top <= 0:
        player_paddle.top = 0


    if player_paddle.bottom >= HEIGHT:
        player_paddle.bottom = HEIGHT


        if opponent_paddle.top <= 0:
            opponent_paddle.top = 0


    if opponent_paddle.bottom >= HEIGHT:
        opponent_paddle.bottom = HEIGHT

    score_text = font.render(f"{opponent_score} - {own_score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))


    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    pygame.display.flip()




pygame.quit()