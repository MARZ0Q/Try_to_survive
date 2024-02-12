

import pygame
import math
pygame.init()

rotate = 0
X = 500
Y = 500

Disp = pygame.display.set_mode((X,Y))

font = pygame.font.Font('freesansbold.ttf', 32)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
 
# set the center of the rectangular object.

def main():
    run = True
    clock = pygame.time.Clock()
    number = 0
    while run:
        number += 1
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        text = font.render(f'{number}', True, green)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2)
        Disp.fill(white)
        Disp.blit(text, textRect)
        pygame.display.update()
    pygame.quit()
main()