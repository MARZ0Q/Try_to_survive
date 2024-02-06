

import pygame
import math
rotate = 0

Disp = pygame.display.set_mode((500,500))

img = pygame.image.load('./First.png').convert()

def rotate3():
    disp = pygame.transform.rotate(img,rotate)
    disp_rect = disp.get_rect(center=(300,300))
    Disp.blit(disp,disp_rect)

def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        rotate3()
        pygame.display.update()
    pygame.quit()
main()