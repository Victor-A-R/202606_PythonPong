import pygame
import asyncio

# Taille de la fenêtre et couleur de fond
WIDTH, HEIGHT = 1000, 1000
BACKGROUND = (0, 0, 0)


WHITE=(255,255,255)
square_size= 20
x, y = WIDTH // 2, HEIGHT // 2
paddle_speed=6
speed_x, speed_y=-5, 5
RED = (250, 50, 80)
paddle_width, paddle_height = 20, 100
paddle_x, paddle_y = WIDTH - 40, HEIGHT // 2 - paddle_height // 2

score = 0

if x > WIDTH:
    running = False

screen = None
font = None
text= None

def init():
    global screen, font, ball_img
    pygame.init()
    screen= pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 36)

    ball_img = pygame.image.load("assets/images/ball.png").convert_alpha()

def update():
    global x, y, speed_x, speed_y, paddle_y, paddle_x, score
    global running

    if (
        speed_x > 0 and
        paddle_x < x + square_size < paddle_x + paddle_width and
        paddle_y < y + square_size and
        y < paddle_y + paddle_height
    ):
        speed_x = -speed_x 
    x = paddle_x - square_size
    score +=1

    # Déplacer la balle
    x += speed_x
    y += speed_y

    # Rebonds haut/ bas
    if y <= 0 or y + square_size >= HEIGHT:
        speed_y = -speed_y

    # Rebonds mur gauche
    if x <= 0:
        speed_x = -speed_x
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle_y > 0:
        paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_y + paddle_height < HEIGHT:
        paddle_y += paddle_speed

def draw():
    screen.fill(BACKGROUND)

    # Dessiner la balle
    centre = (x + square_size // 2, y + square_size // 2)
    rayon = square_size // 2
    pygame.draw.circle(screen, WHITE, centre, rayon)

    pygame.draw.rect(screen, RED, (paddle_x, paddle_y, paddle_width, paddle_height))

    text = font.render(f"Score : {score}", True, WHITE)
    screen.blit(text, (20, 20))
    text = font.render("GAME OVER", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.flip()


def handle_events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False
    return True


async def main():
    global running
    init()
    clock = pygame.time.Clock()
    running = True
    while running:
        running = handle_events()
        update()          # vide pour l’instant
        draw()            # affiche le fond
        clock.tick(60)    # ~60 images/s
        await asyncio.sleep(0)  # indispensable sur le rendu Web

# Démarrage du programme
    asyncio.run(main())
    



    pygame.quit()
