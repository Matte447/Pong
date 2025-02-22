import pygame
import random

# Pygame initialisieren
pygame.init()

dif_ball_speed = 0

# Fenstergröße
WIDTH, HEIGHT = 800, 600

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bildschirm erstellen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Schriftart für das Menü und Spiel
font = pygame.font.Font(None, 50)

# Funktion zum Zeichnen von Text auf dem Bildschirm
def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Menü-Funktion
def menu():
    selected_difficulty = "N"  # Standardmäßig "Normal"
    game_mode = "KI"  # Standardmäßig KI-Gegner

    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Pong Game", WIDTH//2 - 100, 100)
        draw_text("Schwierigkeit wählen:", WIDTH//2 - 200, 200)
        
        # Markierung der gewählten Schwierigkeit
        color_e = WHITE if selected_difficulty == "E" else (100, 100, 100)
        color_n = WHITE if selected_difficulty == "N" else (100, 100, 100)
        color_h = WHITE if selected_difficulty == "H" else (100, 100, 100)
        
        draw_text("E - Einfach", WIDTH//2 - 100, 260, color_e)
        draw_text("N - Normal", WIDTH//2 - 100, 300, color_n)
        draw_text("H - Schwer", WIDTH//2 - 100, 340, color_h)
        
        draw_text("Spielmodus wählen:", WIDTH//2 - 200, 400)
        color_ki = WHITE if game_mode == "KI" else (100, 100, 100)
        color_1v1 = WHITE if game_mode == "1v1" else (100, 100, 100)
        draw_text("1 - KI-Gegner", WIDTH//2 - 100, 440, color_ki)
        draw_text("2 - 1 vs 1", WIDTH//2 - 100, 480, color_1v1)

        draw_text("Drücke Enter zum Starten", WIDTH//2 - 200, 520)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    selected_difficulty = "E"
                if event.key == pygame.K_n:
                    selected_difficulty = "N"
                if event.key == pygame.K_h:
                    selected_difficulty = "H"
                if event.key == pygame.K_1:
                    game_mode = "KI"
                if event.key == pygame.K_2:
                    game_mode = "1v1"
                if event.key == pygame.K_RETURN:
                    running = False  # Menü verlassen und Spiel starten

    return selected_difficulty, game_mode  # Schwierigkeit und Spielmodus zurückgeben

# Menü starten und Einstellungen übernehmen
difficulty, game_mode = menu()

# Schwierigkeitseinstellungen
if difficulty == "E":
    dif_ball_speed = 3
    ball_speed = 3
    PADDLE_SPEED = 5
elif difficulty == "N":
    dif_ball_speed = 5
    ball_speed = 5
    PADDLE_SPEED = 7
elif difficulty == "H":
    dif_ball_speed = 7
    ball_speed = 7
    PADDLE_SPEED = 9

print(f"Schwierigkeit: {difficulty}, Spielmodus: {game_mode}")

# Spielvariablen
own_score = 0
opponent_score = 0

# Ball und Schläger erstellen
ball = pygame.Rect(WIDTH//2 - 10, random.randint(0, HEIGHT-20), 20, 20)
player_paddle = pygame.Rect(WIDTH - 20, HEIGHT//2 - 50, 10, 100)
opponent_paddle = pygame.Rect(10, HEIGHT//2 - 50, 10, 100)

# Ballbewegung
ball_dx, ball_dy = random.choice([-ball_speed, ball_speed]), random.choice([-ball_speed, ball_speed])

# Countdown vor Spielbeginn
countdown_font = pygame.font.Font(None, 60)
for i in range(3, 0, -1):
    screen.fill(BLACK)
    draw_text(str(i), WIDTH//2 - 20, HEIGHT//2 - 30)
    pygame.display.flip()
    pygame.time.delay(1000)

# Spiel-Loop
running = True
while running:
    pygame.time.delay(16)
    screen.fill(BLACK)

    # Event-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spielerbewegung
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED

    
    


    # Ballbewegung
    ball.x += ball_dx
    ball.y += ball_dy

    # Ball prallt an Decke und Boden ab
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_dx *= -1
        ball_speed *= 1.01  # Ball wird schneller

        # Geschwindigkeit aktualisieren
        ball_dx = (ball_dx / abs(ball_dx)) * ball_speed
        ball_dy = (ball_dy / abs(ball_dy)) * ball_speed

        print(ball_speed)




    # Punkt für Gegner
    if ball.left <= 0:
        opponent_score += 1
        ball.x, ball.y = WIDTH//2 - 10, random.randint(0, HEIGHT-20)
        ball_dx, ball_dy = random.choice([-ball_speed, ball_speed]), random.choice([-ball_speed, ball_speed])
        player_paddle.y, opponent_paddle.y = HEIGHT//2 - 50, HEIGHT//2 - 50
        ball_speed = dif_ball_speed
        print(ball_speed)

    # Punkt für Spieler
    if ball.right >= WIDTH:
        own_score += 1
        ball.x, ball.y = WIDTH//2 - 10, random.randint(0, HEIGHT-20)
        ball_dx, ball_dy = random.choice([-ball_speed, ball_speed]), random.choice([-ball_speed, ball_speed])
        player_paddle.y, opponent_paddle.y = HEIGHT//2 - 50, HEIGHT//2 - 50
        ball_speed = dif_ball_speed
        print(ball_speed)

    # Gegner-KI bewegt sich zum Ball
    if game_mode == "KI":
        if ball_dx < 0:  # Ball bewegt sich nach links zur KI
            frames_until_impact = abs((opponent_paddle.x - ball.x) / ball_dx)  # Wie lange dauert es, bis der Ball ankommt?
            predicted_y = ball.y + (ball_dy * frames_until_impact)  # Wo landet der Ball?

            # Fehler hinzufügen, damit die KI nicht zu perfekt ist
            error_margin = random.randint(-65, 65)
            predicted_y += error_margin

            # Begrenzung, damit die KI nicht über das Spielfeld hinausgeht
            predicted_y = max(0, min(HEIGHT, predicted_y))

            # Bewegen der KI
            if opponent_paddle.centery < predicted_y:
                opponent_paddle.y += PADDLE_SPEED - 2
            elif opponent_paddle.centery > predicted_y:
                opponent_paddle.y -= PADDLE_SPEED - 2
    else:
        if keys[pygame.K_w] and opponent_paddle.top > 0:
            opponent_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and opponent_paddle.bottom < HEIGHT:
            opponent_paddle.y += PADDLE_SPEED

    if opponent_paddle.top < 0:
        opponent_paddle.top = 0
    if opponent_paddle.bottom > HEIGHT:
        opponent_paddle.bottom = HEIGHT

    # Punktestand anzeigen
    score_text = font.render(f"{opponent_score} - {own_score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    # Spielfeld zeichnen
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    pygame.display.flip()

pygame.quit()
