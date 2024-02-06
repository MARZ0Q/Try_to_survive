
import pygame

HEIGHT = 500
WIDTH = 1000

pygame.display.set_caption('Try to survive')
DISP = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.init()

BACKGROUND_IMAGE_WIDTH = WIDTH*6
BACKGROUND_IMAGE_HEIGHT = WIDTH*6

VEL = 20
FPS = 60
BLACK = (0,0,0)
MC_WIDTH = WIDTH/6
MC_HEIGHT = WIDTH/6
BLACK = (0,0,0)
BACKGROUND_IMAGE = pygame.image.load('./Background.jpg')
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE,(BACKGROUND_IMAGE_WIDTH,BACKGROUND_IMAGE_HEIGHT))
MC_image = pygame.image.load('./First.png')
MC = pygame.transform.scale(MC_image,(MC_WIDTH,MC_HEIGHT))


def draw_window():
    DISP.fill(BLACK)

def draw_character_and_background(mc_rect,background_rect):
    DISP.blit(BACKGROUND,(background_rect.x,background_rect.y))
    DISP.blit(MC,(mc_rect.x,mc_rect.y))

def move_character(background_rect):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        background_rect.x=background_rect.x+VEL
    if keys[pygame.K_RIGHT]:
        background_rect.x=background_rect.x-VEL
    if keys[pygame.K_UP]:
        background_rect.y=background_rect.y+VEL
    if keys[pygame.K_DOWN]:
        background_rect.y=background_rect.y-VEL

    pygame.display.update()

def game_border(background_rect):
    if background_rect.y < HEIGHT/2-BACKGROUND_IMAGE_HEIGHT+MC_HEIGHT:
        background_rect.y = HEIGHT/2-BACKGROUND_IMAGE_HEIGHT+MC_HEIGHT

    if background_rect.y > 0+MC_HEIGHT:
        background_rect.y = 0+MC_HEIGHT

    if background_rect.x < WIDTH/2-BACKGROUND_IMAGE_WIDTH+MC_WIDTH:
        background_rect.x = WIDTH/2-BACKGROUND_IMAGE_WIDTH+MC_WIDTH

    if background_rect.x > 0+MC_WIDTH*2:
        background_rect.x = 0+MC_WIDTH*2

def main():
    mc_rect = pygame.Rect(WIDTH/2-(WIDTH/6/2),HEIGHT/2-(HEIGHT/4/2),MC_WIDTH,MC_HEIGHT)
    background_rect = pygame.Rect(WIDTH/2-(BACKGROUND_IMAGE_WIDTH/2),HEIGHT/2-(BACKGROUND_IMAGE_HEIGHT/2),BACKGROUND_IMAGE_WIDTH,BACKGROUND_IMAGE_HEIGHT)
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()
        game_border(background_rect)
        draw_character_and_background(mc_rect,background_rect)
        move_character(background_rect)

    pygame.quit()



main()

if __name__ == '__python.py__':
    main()