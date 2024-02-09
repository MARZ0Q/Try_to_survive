
import pygame
import math 
import random

HEIGHT = 700
WIDTH = 700

pygame.display.set_caption('Try to survive')
DISP = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.init()


VEL = 12
FPS = 60
WHITE = (255,255,255)
MC_WIDTH = WIDTH/6
MC_HEIGHT = WIDTH/6
BLACK = (0,0,0)
DARKNESS_WIDTH = WIDTH*1.5
DARKNESS_HEIGHT = WIDTH*1.5
BACKGROUND_WIDTH = WIDTH*6
BACKGROUND_HEIGHT = WIDTH*6
MONSTER_WIDTH = WIDTH/6
MONSTER_HEIGHT = HEIGHT/6
MONSTER_VEL = 9
MONSTER_MAX_RANGE = 100
MONSTER_BORDER_UP_Y = (HEIGHT/2-BACKGROUND_HEIGHT/2)+MONSTER_HEIGHT
MONSTER_BORDER_DOWN_Y = (-HEIGHT/2+BACKGROUND_HEIGHT/2)+WIDTH-MONSTER_HEIGHT
MONSTER_BORDER_LEFT_X = (WIDTH/2-BACKGROUND_WIDTH/2)+MONSTER_WIDTH
MONSTER_BORDER_RIGHT_X = (-WIDTH/2+BACKGROUND_WIDTH/2)+WIDTH-MONSTER_WIDTH

BACKGROUND_IMAGE = pygame.image.load('./Background.jpg')
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE,(BACKGROUND_WIDTH,BACKGROUND_HEIGHT))
MC_IMAGE = pygame.image.load('./First.png')
MC = pygame.transform.scale(MC_IMAGE,(MC_WIDTH,MC_HEIGHT)).convert_alpha()
DARKNESS_IMAGE = pygame.image.load('./Darkness.png').convert_alpha()
DARKNESS = pygame.transform.scale(DARKNESS_IMAGE,(DARKNESS_WIDTH,DARKNESS_HEIGHT))

monster_decision_x_neg_or_pos = random.choice([1,-1])
monster_decision_y_neg_or_pos = random.choice([1,-1])
monster_decision_range = random.randint(1,MONSTER_MAX_RANGE)
monster_previous_position_x = 0
monster_previous_position_y = 0
monster_location_getting_time = 0
monster_mc_collision = False
detected = False
range_adder = random.choice([66,100])

MONSTER_IMAGE = pygame.image.load('./First.png')
MONSTER = pygame.transform.scale(MONSTER_IMAGE,(MONSTER_WIDTH,MONSTER_HEIGHT)).convert_alpha()

def draw_window():
    DISP.fill(WHITE)

def draw_characters(mc_rect):
    pos = pygame.mouse.get_pos()
    x_dist = pos[0] - 300
    y_dist = (pos[1]-300)
    rotate = math.degrees(math.atan2(x_dist,y_dist))+180
    mc_rotate = pygame.transform.rotate(MC,rotate)
    mc_center_rect = mc_rotate.get_rect(center = (mc_rect.x+MC_WIDTH/2,mc_rect.y+MC_HEIGHT/2))
    DISP.blit(mc_rotate,(mc_center_rect))


def move_characters(background_rect,monster_rect):
    global monster_previous_position_x
    global monster_previous_position_y
    global MONSTER_BORDER_UP_Y
    global MONSTER_BORDER_DOWN_Y
    global MONSTER_BORDER_LEFT_X
    global MONSTER_BORDER_RIGHT_X

    # background movement
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        background_rect.x=background_rect.x+VEL
        if background_rect.x < 0+MC_WIDTH*2:
            MONSTER_BORDER_LEFT_X += VEL
            MONSTER_BORDER_RIGHT_X += VEL
            
    if keys[pygame.K_RIGHT]:
        background_rect.x=background_rect.x-VEL
        if background_rect.x > WIDTH/2-BACKGROUND_WIDTH+MC_WIDTH:
            MONSTER_BORDER_RIGHT_X -= VEL
            MONSTER_BORDER_LEFT_X -= VEL

    if keys[pygame.K_UP]:
        background_rect.y=background_rect.y+VEL
        if background_rect.y < 0+MC_HEIGHT:
            MONSTER_BORDER_DOWN_Y += VEL
            MONSTER_BORDER_UP_Y += VEL
        # MONSTER_BORDER_UP_Y += VEL
    if keys[pygame.K_DOWN]:
        background_rect.y=background_rect.y-VEL
        if background_rect.y > HEIGHT/2-BACKGROUND_HEIGHT+MC_HEIGHT:
            MONSTER_BORDER_DOWN_Y -= VEL
            MONSTER_BORDER_UP_Y -= VEL
    
    # monster movement
    if keys[pygame.K_LEFT]:
        if background_rect.x < 0+MC_WIDTH*2:
            monster_rect.x=monster_rect.x+VEL
            monster_previous_position_x = monster_previous_position_x + VEL
    if keys[pygame.K_RIGHT]:
        if background_rect.x > WIDTH/2-BACKGROUND_WIDTH+MC_WIDTH:
            monster_rect.x=monster_rect.x-VEL
            monster_previous_position_x = monster_previous_position_x - VEL
    if keys[pygame.K_UP]:
        if background_rect.y < 0+MC_HEIGHT:
            monster_rect.y=monster_rect.y+VEL
            monster_previous_position_y = monster_previous_position_y + VEL     
    if keys[pygame.K_DOWN]:
        if background_rect.y > HEIGHT/2-BACKGROUND_HEIGHT+MC_HEIGHT:
            monster_rect.y=monster_rect.y-VEL
            monster_previous_position_y = monster_previous_position_y - VEL



def game_border_and_draw_background(background_rect):
    DISP.blit(BACKGROUND,(background_rect.x,background_rect.y))

    if background_rect.y < HEIGHT/2-BACKGROUND_HEIGHT+MC_HEIGHT:
        background_rect.y = HEIGHT/2-BACKGROUND_HEIGHT+MC_HEIGHT

    if background_rect.y > 0+MC_HEIGHT:
        background_rect.y = 0+MC_HEIGHT

    if background_rect.x < WIDTH/2-BACKGROUND_WIDTH+MC_WIDTH:
        background_rect.x = WIDTH/2-BACKGROUND_WIDTH+MC_WIDTH

    if background_rect.x > 0+MC_WIDTH*2:
        background_rect.x = 0+MC_WIDTH*2

def draw_darkness(mc_rect):
    pos = pygame.mouse.get_pos()
    x_dist = pos[0] - 300
    y_dist = (pos[1]-300)
    rotate = math.degrees(math.atan2(x_dist,y_dist))-180
    darkness = pygame.transform.rotate(DARKNESS,rotate)
    darkness_center_rect = darkness.get_rect(center = (mc_rect.x+MC_WIDTH/2,mc_rect.y+MC_HEIGHT/2))
    DISP.blit(darkness,(darkness_center_rect))

def draw_monster(monster_rect,mc_rect):
    global detected

    pos = pygame.mouse.get_pos()
    x_dist = pos[0]-300
    y_dist = (pos[1]-300)
    rotate = math.degrees(math.atan2(x_dist,y_dist))-180
    monster_x_dist = monster_rect.x - 300
    monster_y_dist = (monster_rect.y-300)
    monster_rotate = math.degrees(math.atan2(monster_x_dist,monster_y_dist))-180

    if abs(rotate)+20+2>abs(monster_rotate)>abs(rotate)-20-16 and abs(mc_rect.x-monster_rect.x)<379 and abs(mc_rect.y-monster_rect.y)<418:
        detected = True
        # pass
    if detected == False:
        roam(monster_rect)
        monster_rotation(monster_rect)
        # pass

    # DISP.blit(MONSTER,(monster_rect.x,monster_rect.y))

def roam(monster_rect):
    global monster_decision_x_neg_or_pos
    global monster_decision_y_neg_or_pos
    global monster_decision_range
    global monster_previous_position_x
    global monster_previous_position_y
    global monster_location_getting_time
    global range_adder

    if monster_location_getting_time == 0:        
        monster_previous_position_x = monster_rect.x
        monster_previous_position_y = monster_rect.y
        monster_location_getting_time = 1

    # For random x
    if monster_decision_x_neg_or_pos >0:
        if abs(abs(monster_rect.x) - abs(monster_previous_position_x)-monster_decision_range) <= monster_decision_range:
            monster_rect.x += MONSTER_VEL
        else:
            monster_decision_range = random.randint(1,MONSTER_MAX_RANGE)
            monster_decision_x_neg_or_pos = random.choice([1,-1])
            monster_location_getting_time = 0
            monster_decision_y_neg_or_pos = random.choice([1,-1])
            range_adder= random.choice([100,0])
    
    if monster_decision_x_neg_or_pos <0:
        if abs(abs(monster_rect.x) -abs(monster_previous_position_x)-monster_decision_range) <= monster_decision_range+range_adder:
            monster_rect.x -= MONSTER_VEL
        else:
            monster_decision_range = random.randint(1,MONSTER_MAX_RANGE)
            monster_decision_x_neg_or_pos = random.choice([1,-1])
            monster_decision_y_neg_or_pos = random.choice([1,-1])
            monster_location_getting_time = 0
            range_adder= random.choice([100,0])

        
   # For random y
    if monster_decision_y_neg_or_pos >0:
        if abs(abs(monster_rect.y) - abs(monster_previous_position_y)-monster_decision_range) <= monster_decision_range:
            monster_rect.y += MONSTER_VEL
        else:
            monster_decision_range = random.randint(1,MONSTER_MAX_RANGE)
            monster_decision_y_neg_or_pos = random.choice([1,-1])
            monster_decision_x_neg_or_pos = random.choice([1,-1])
            monster_location_getting_time = 0
            range_adder= random.choice([100,0])
    
    if monster_decision_y_neg_or_pos <0:
        if abs(abs(monster_rect.y) -abs(monster_previous_position_y)-monster_decision_range) <= monster_decision_range+range_adder:
            monster_rect.y -= MONSTER_VEL
        else:
            monster_decision_range = random.randint(1,MONSTER_MAX_RANGE)
            monster_decision_y_neg_or_pos = random.choice([1,-1])
            monster_decision_x_neg_or_pos = random.choice([1,-1])
            monster_location_getting_time = 0
            range_adder= random.choice([100,0])

def monsters_border(monster_rect,background_rect):
    global monster_decision_range

    if MONSTER_BORDER_UP_Y>monster_rect.y:
        monster_rect.y = MONSTER_BORDER_UP_Y+MONSTER_HEIGHT
        monster_decision_range = -100
    if MONSTER_BORDER_DOWN_Y<monster_rect.y:
        monster_rect.y = MONSTER_BORDER_DOWN_Y-MONSTER_HEIGHT
        monster_decision_range = -100

    if MONSTER_BORDER_LEFT_X>monster_rect.x:
        monster_rect.x = MONSTER_BORDER_LEFT_X+MONSTER_WIDTH
        monster_decision_range = -100
    if MONSTER_BORDER_RIGHT_X<monster_rect.x:
        monster_rect.x = MONSTER_BORDER_RIGHT_X-MONSTER_WIDTH
        monster_decision_range = -100

def monster_rotation(monster_rect):
    x_dist = -abs(monster_rect.x)+abs(monster_previous_position_x)
    y_dist = -abs(monster_rect.y)+abs(monster_previous_position_y)
    rotate = math.degrees(math.atan2(x_dist,y_dist))
    monster_rotate = pygame.transform.rotate(MONSTER,rotate)
    monster_center_rect = monster_rotate.get_rect(center = (monster_rect.x+MONSTER_WIDTH/2,monster_rect.y+MONSTER_HEIGHT/2))
    DISP.blit(monster_rotate,monster_center_rect)

def draw_mask_and_detection(monster_rect,mc_rect):
    global monster_mc_collision

    pos = pygame.mouse.get_pos()
    x_dist_mc = pos[0] - 300
    y_dist_mc = (pos[1]-300)
    rotate = math.degrees(math.atan2(x_dist_mc,y_dist_mc))+180
    mc_rotate = pygame.transform.rotate(MC,rotate)
    mc_center_rect = mc_rotate.get_rect(center = (mc_rect.x+MC_WIDTH/2,mc_rect.y+MC_HEIGHT/2))


    x_dist = -abs(monster_rect.x)+abs(monster_previous_position_x)
    y_dist = -abs(monster_rect.y)+abs(monster_previous_position_y)
    rotate = math.degrees(math.atan2(x_dist,y_dist))
    monster_rotate = pygame.transform.rotate(MONSTER,rotate)
    monster_center_rect = monster_rotate.get_rect(center = (monster_rect.x+MONSTER_WIDTH/2,monster_rect.y+MONSTER_HEIGHT/2))

    monster_mask = pygame.mask.from_surface(monster_rotate)
    monster_image = monster_mask.to_surface()
    mc_mask = pygame.mask.from_surface(mc_rotate)
    mc_image = mc_mask.to_surface()

    DISP.blit(monster_image,monster_center_rect)
    DISP.blit(mc_image,mc_center_rect)

    if monster_mask.overlap(mc_mask,(mc_rect.x-monster_rect.x,mc_rect.y-monster_rect.y)):
        monster_mc_collision = True

def chase(monster_rect,mc_rect):

    if monster_rect.x< mc_rect.x:
        monster_rect.x += MONSTER_VEL
    elif monster_rect.x> mc_rect.x:
        monster_rect.x-= MONSTER_VEL

    if monster_rect.y< mc_rect.y:
        monster_rect.y += MONSTER_VEL
    elif monster_rect.y> mc_rect.y:
        monster_rect.y-= MONSTER_VEL

    monster_rotation(monster_rect)

def main():
    mc_rect = pygame.Rect(WIDTH/2-(WIDTH/6/2),HEIGHT/2-(HEIGHT/4/2),MC_WIDTH,MC_HEIGHT)
    monster_rect = pygame.Rect(WIDTH/2,HEIGHT/2,MONSTER_WIDTH,MONSTER_HEIGHT)
    background_rect = pygame.Rect(WIDTH/2-(BACKGROUND_WIDTH/2),HEIGHT/2-(BACKGROUND_HEIGHT/2),BACKGROUND_WIDTH,BACKGROUND_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or monster_mc_collision:
                run = False

        draw_window()
        draw_mask_and_detection(monster_rect,mc_rect)
        game_border_and_draw_background(background_rect)
        move_characters(background_rect,monster_rect)
        # draw_darkness(mc_rect)
        if detected == True:
            chase(monster_rect,mc_rect)

        monsters_border(monster_rect,background_rect)
        draw_monster(monster_rect,mc_rect)
        draw_characters(mc_rect)
        pygame.display.update()

    pygame.quit()



main()

# if __name__ == '__python.py__':
#     main()