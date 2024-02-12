import pygame
import math 
import random
import threading
import sys
import tkinter as tk

pygame.init()

window  = tk.Tk()

ABSOLUTE_PATH = 'Try_to_survive'
HEIGHT = 700
WIDTH = 700

BAD_ENDING_PIC = pygame.image.load('./bad_ending.png') 
BAD_ENDING_SCALED_PIC = pygame.transform.scale(BAD_ENDING_PIC,(WIDTH,HEIGHT))
pygame.display.set_caption('Try to survive')
DISP = pygame.display.set_mode((WIDTH,HEIGHT))

number_of_collected_flesh = 0

RED  = (255,0,0)
BLACK = (0,0,0)

FPS = 30
VEL = 13
WHITE = (255,255,255)
MC_WIDTH = WIDTH/6
MC_HEIGHT = WIDTH/6

FLESH_WIDTH = WIDTH/6
FLESH_HEIGHT = HEIGHT/6

DARKNESS_WIDTH = WIDTH*1.5
DARKNESS_HEIGHT = WIDTH*1.5
BACKGROUND_WIDTH = WIDTH*6
BACKGROUND_HEIGHT = WIDTH*6
MONSTER_WIDTH = WIDTH/6
MONSTER_HEIGHT = HEIGHT/6
FONT = pygame.font.Font('freesansbold.ttf', 32)
MONSTER_VEL = 13
MONSTER_MAX_RANGE = 100
MONSTER_BORDER_UP_Y = (HEIGHT/2-BACKGROUND_HEIGHT/2)+MONSTER_HEIGHT
MONSTER_BORDER_DOWN_Y = (-HEIGHT/2+BACKGROUND_HEIGHT/2)+WIDTH-MONSTER_HEIGHT
MONSTER_BORDER_LEFT_X = (WIDTH/2-BACKGROUND_WIDTH/2)+MONSTER_WIDTH/2
MONSTER_BORDER_RIGHT_X = (-WIDTH/2+BACKGROUND_WIDTH/2)+WIDTH-MONSTER_WIDTH
MONSTER_HELPER_WIDTH = WIDTH/6
MONSTER_HELPER_HEIGHT = HEIGHT/6
MONSTER_HELPER_IMAGE = pygame.image.load('./funny_looking_ghost.png')
MONSTER_HELPER = pygame.transform.scale(MONSTER_HELPER_IMAGE,(MONSTER_HELPER_WIDTH,MONSTER_HEIGHT))
BACKGROUND_IMAGE = pygame.image.load('./Background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE,(BACKGROUND_WIDTH,BACKGROUND_HEIGHT))
MC_IMAGE = pygame.image.load('./First_1.png')
MC = pygame.transform.scale(MC_IMAGE,(MC_WIDTH,MC_HEIGHT)).convert_alpha()
DARKNESS_IMAGE = pygame.image.load('./Darkness.png').convert_alpha()
DARKNESS = pygame.transform.scale(DARKNESS_IMAGE,(DARKNESS_WIDTH,DARKNESS_HEIGHT))
MONSTER_HELPER_MAX_RANGE = 250

pygame.mixer.init()

# sounds
HEART_BEAT_SOUND = pygame.mixer.Sound('./heart-beat.mp3')
WHISTLE_SOUND_1 = pygame.mixer.Sound('./whistle-one.mp3')
WHISTLE_SOUND_2 = pygame.mixer.Sound('./whistle-two.mp3')

monster_helper_detection = False
should_helper_monster_decision_continue = True
monster_helper_spawned = False
monster_decision_x_neg_or_pos = random.choice([1,-1])
monster_decision_y_neg_or_pos = random.choice([1,-1])
monster_helper_mid_pos_decision = random.choice([True,False])

monster_decision_range = random.randint(1,MONSTER_MAX_RANGE)
monster_previous_position_x = 0
monster_previous_position_y = 0
monster_location_getting_time = 0
monster_mc_collision = False
detected = False
range_adder_choice = [100,-100,0]
range_adder = random.choice(range_adder_choice)
has_monster_helper_spawned = False
monster_decision_to_spawn = random.randint(1,1000)
monster_initial_decision_to_spawn = random.choice(['t-r','b-l'])
monster_in_game_decision_to_spawn = random.choice(['t-r','b-l'])
monster_helper_draw_time = 0
despawn_timer = 2
mc_previous_rect_x = 0
mc_previous_rect_y = 0
mc_previous_position_getting_time = 0

monster_relief_musice_play_times = 0

MONSTER_IMAGE = pygame.image.load('./Monster.png')
MONSTER = pygame.transform.scale(MONSTER_IMAGE,(MONSTER_WIDTH,MONSTER_HEIGHT)).convert_alpha()
monster_relief = pygame.mixer.Sound('./monster_relief.mp3')

FLESH_IMAGE = pygame.image.load('./Monster.png')
FLESH = pygame.transform.scale(MONSTER_IMAGE,(MONSTER_WIDTH,MONSTER_HEIGHT))


monster_helper_decision_to_spawn = random.randint(1,3)

flesh_initial_spawn_funcion_times = 0

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


def move_characters(background_rect,monster_rect,flesh1_rect):
    global monster_previous_position_x
    global monster_previous_position_y
    global MONSTER_BORDER_UP_Y
    global MONSTER_BORDER_DOWN_Y
    global MONSTER_BORDER_LEFT_X
    global MONSTER_BORDER_RIGHT_X
    global mc_previous_rect_x
    global mc_previous_rect_y
    

    # background movement
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        background_rect.x=background_rect.x+VEL
        if background_rect.x < 0+MC_WIDTH*2:
            flesh1_rect.x +=VEL
        mc_previous_rect_x +=VEL
        if background_rect.x < 0+MC_WIDTH*2:
            MONSTER_BORDER_LEFT_X += VEL
            MONSTER_BORDER_RIGHT_X += VEL
            
    if keys[pygame.K_RIGHT]:
        background_rect.x=background_rect.x-VEL
        if background_rect.x > WIDTH/2-BACKGROUND_WIDTH+MC_WIDTH:
            flesh1_rect.x -=VEL
        mc_previous_rect_x -=VEL
        if background_rect.x > WIDTH/2-BACKGROUND_WIDTH+MC_WIDTH:
            MONSTER_BORDER_RIGHT_X -= VEL
            MONSTER_BORDER_LEFT_X -= VEL

    if keys[pygame.K_UP]:
        background_rect.y=background_rect.y+VEL
        if  background_rect.y < 0+MC_HEIGHT:
            flesh1_rect.y += VEL
        mc_previous_rect_y +=VEL
        if background_rect.y < 0+MC_HEIGHT:
            MONSTER_BORDER_DOWN_Y += VEL
            MONSTER_BORDER_UP_Y += VEL
        # MONSTER_BORDER_UP_Y += VEL
    if keys[pygame.K_DOWN]:
        background_rect.y=background_rect.y-VEL
        if background_rect.y > HEIGHT/2-BACKGROUND_HEIGHT+MC_HEIGHT:
            flesh1_rect.y -= VEL
        mc_previous_rect_y -=VEL
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



def game_border_and_draw_background(background_rect,flesh1_rect):
    DISP.blit(BACKGROUND,(background_rect.x,background_rect.y))

    if background_rect.y < HEIGHT/2-BACKGROUND_HEIGHT+MC_HEIGHT:
        background_rect.y = HEIGHT/2-BACKGROUND_HEIGHT+MC_HEIGHT

    if background_rect.y > 0+MC_HEIGHT:
        background_rect.y = 0+MC_HEIGHT
        flesh1_rect.y = 0+MC_HEIGHT

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
    elif  monster_helper_detection and not detected:
        chase_when_monster_helper_detection(monster_rect,mc_rect)
    elif detected == False:
        roam(monster_rect)
        monster_rotation(monster_rect)

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
            range_adder= random.choice(range_adder_choice)
    
    if monster_decision_x_neg_or_pos <0:
        if abs(abs(monster_rect.x) -abs(monster_previous_position_x)-monster_decision_range) <= monster_decision_range+range_adder:
            monster_rect.x -= MONSTER_VEL
        else:
            monster_decision_range = random.randint(1,MONSTER_MAX_RANGE)
            monster_decision_x_neg_or_pos = random.choice([1,-1])
            monster_decision_y_neg_or_pos = random.choice([1,-1])
            monster_location_getting_time = 0
            range_adder= random.choice(range_adder_choice)

        
   # For random y
    if monster_decision_y_neg_or_pos >0:
        if abs(abs(monster_rect.y) - abs(monster_previous_position_y)-monster_decision_range) <= monster_decision_range:
            monster_rect.y += MONSTER_VEL
        else:
            monster_decision_range = random.randint(1,MONSTER_MAX_RANGE)
            monster_decision_y_neg_or_pos = random.choice([1,-1])
            monster_decision_x_neg_or_pos = random.choice([1,-1])
            monster_location_getting_time = 0
            range_adder= random.choice(range_adder_choice)
    
    if monster_decision_y_neg_or_pos <0:
        if abs(abs(monster_rect.y) -abs(monster_previous_position_y)-monster_decision_range) <= monster_decision_range+range_adder:
            monster_rect.y -= MONSTER_VEL
        else:
            monster_decision_range = random.randint(1,MONSTER_MAX_RANGE)
            monster_decision_y_neg_or_pos = random.choice([1,-1])
            monster_decision_x_neg_or_pos = random.choice([1,-1])
            monster_location_getting_time = 0
            range_adder= random.choice(range_adder_choice)


def monsters_border(monster_rect):
    global monster_decision_range

    if MONSTER_BORDER_UP_Y>monster_rect.y - MONSTER_VEL:
        monster_rect.y = MONSTER_BORDER_UP_Y +10
        monster_decision_range = 0
    if MONSTER_BORDER_DOWN_Y<monster_rect.y + MONSTER_VEL:
        monster_rect.y = MONSTER_BORDER_DOWN_Y -10
        monster_decision_range = 0

    if MONSTER_BORDER_LEFT_X>monster_rect.x - MONSTER_VEL:
        monster_rect.x = MONSTER_BORDER_LEFT_X +10
        monster_decision_range = 0
    if MONSTER_BORDER_RIGHT_X<monster_rect.x + MONSTER_VEL:
        monster_rect.x = MONSTER_BORDER_RIGHT_X -10
        monster_decision_range = 0

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

def monster_chase_rotation(monster_rect,mc_rect):
    x_dist = abs(monster_rect.x)-abs(mc_rect.x)
    y_dist = abs(monster_rect.y)-abs(mc_rect.y)
    monster_rotation = math.degrees(math.atan2(x_dist,y_dist))
    monster_rotate = pygame.transform.rotate(MONSTER,monster_rotation)
    monster_center_rect = monster_rotate.get_rect(center = (monster_rect.x+MONSTER_WIDTH/2,monster_rect.y+MONSTER_HEIGHT/2))
    DISP.blit(monster_rotate,monster_center_rect)



def chase(monster_rect,mc_rect):

    if monster_rect.x< mc_rect.x:
        monster_rect.x += MONSTER_VEL
    elif monster_rect.x> mc_rect.x:
        monster_rect.x-= MONSTER_VEL

    if monster_rect.y< mc_rect.y:
        monster_rect.y += MONSTER_VEL
    elif monster_rect.y> mc_rect.y:
        monster_rect.y-= MONSTER_VEL

    monster_chase_rotation(monster_rect,mc_rect)

def monster_mid_game_decision_to_spawn(monster_rect,bottom_left_spawn_rect,top_right_spawn_rect):
    global monster_decision_to_spawn
    global monster_in_game_decision_to_spawn

    monster_decision_to_spawn = random.randint(1,1000)
    monster_in_game_decision_to_spawn = random.choice(['t-r','b-l'])

    if monster_decision_to_spawn == 5 and monster_in_game_decision_to_spawn == 't-r':
        monster_rect.x = top_right_spawn_rect.x
        monster_rect.y = top_right_spawn_rect.y
    
    if monster_decision_to_spawn == 5 and monster_in_game_decision_to_spawn == 'b-l':
        monster_rect.x = bottom_left_spawn_rect.x
        monster_rect.y = bottom_left_spawn_rect.y


def draw_monster_helper(mc_rect):
    global monster_helper_draw_time
    global monster_helper_x_neg_or_pos_decision
    global monster_helper_y_neg_or_pos_decision
    global monster_helper_mid_pos_decision

    monster_helper_rect = pygame.Rect(WIDTH/2-(WIDTH/6/2),HEIGHT/2-(HEIGHT/4/2),MONSTER_HELPER_WIDTH,MONSTER_HELPER_HEIGHT)


    if monster_helper_draw_time == 0:
        monster_helper_x_neg_or_pos_decision = random.choice([1,-1])
        monster_helper_y_neg_or_pos_decision = random.choice([1,-1])
        monster_helper_mid_pos_decision = random.choice([True,False])
        monster_helper_draw_time = 1

    if monster_helper_x_neg_or_pos_decision > 0:
        monster_helper_rect.x = monster_helper_rect.x + MONSTER_HELPER_MAX_RANGE
    elif monster_helper_x_neg_or_pos_decision < 0:
        monster_helper_rect.x = monster_helper_rect.x - MONSTER_HELPER_MAX_RANGE

    if monster_helper_y_neg_or_pos_decision > 0:
        monster_helper_rect.y = monster_helper_rect.y +MONSTER_HELPER_MAX_RANGE
    elif monster_helper_y_neg_or_pos_decision < 0:
        monster_helper_rect.y = monster_helper_rect.y - MONSTER_HELPER_MAX_RANGE



    if monster_helper_mid_pos_decision and monster_helper_x_neg_or_pos_decision > 0 and monster_helper_y_neg_or_pos_decision :
        monster_helper_rect.x = mc_rect.x + MONSTER_HELPER_MAX_RANGE
        monster_helper_rect.y = mc_rect.y

    if monster_helper_mid_pos_decision and monster_helper_x_neg_or_pos_decision < 0 and monster_helper_y_neg_or_pos_decision > 0:
        monster_helper_rect.x = mc_rect.x - MONSTER_HELPER_MAX_RANGE
        monster_helper_rect.y = mc_rect.y

    if monster_helper_mid_pos_decision and monster_helper_x_neg_or_pos_decision < 0 and monster_helper_y_neg_or_pos_decision < 0:
        monster_helper_rect.y = mc_rect.y - MONSTER_HELPER_MAX_RANGE
        monster_helper_rect.x = mc_rect.x

    if monster_helper_mid_pos_decision and monster_helper_x_neg_or_pos_decision > 0 and monster_helper_y_neg_or_pos_decision > 0:
        monster_helper_rect.y = mc_rect.y + MONSTER_HELPER_MAX_RANGE
        monster_helper_rect.x = mc_rect.x

    DISP.blit(MONSTER_HELPER,(monster_helper_rect.x,monster_helper_rect.y))
    monster_helper_detection_func(monster_helper_rect.x,monster_helper_rect.y)

def monster_helper_decision():
    global monster_helper_decision_to_spawn
    monster_helper_decision_to_spawn = random.randint(1,3)

    if monster_helper_decision_to_spawn == 1:
        return True
    else:
        return False

def spawn_monster_helper():
    global should_helper_monster_decision_continue
    global monster_helper_draw_time

    should_helper_monster_decision_continue = True
    monster_helper_draw_time = 0
    

def despawn_monster_helper():
    global has_monster_helper_spawned
    has_monster_helper_spawned = False
    monster_helper_spawn_delay = random.randint(1,10)
    monster_helper_delay= threading.Timer(monster_helper_spawn_delay, spawn_monster_helper)
    monster_helper_delay.start()


def monster_helper_detection_func(monster_helper_rect_x,monster_helper_rect_y):
    global monster_helper_detection

    pos = pygame.mouse.get_pos()
    x_dist = pos[0]-300
    y_dist = (pos[1]-300)
    rotate = math.degrees(math.atan2(x_dist,y_dist))-180
    monster_x_dist = monster_helper_rect_x - 300
    monster_y_dist = (monster_helper_rect_y-300)
    monster_rotate = math.degrees(math.atan2(monster_x_dist,monster_y_dist))-180

    if abs(rotate)+20+2>abs(monster_rotate)>abs(rotate)-20-16:
        monster_helper_detection = True

def chase_when_monster_helper_detection(monster_rect,mc_rect):
    global mc_previous_rect_x
    global mc_previous_rect_y
    global mc_previous_position_getting_time
    global monster_helper_detection

    if mc_previous_position_getting_time ==0:
        mc_previous_rect_x = mc_rect.x
        mc_previous_rect_y = mc_rect.y
        play_whistle_sound()
        mc_previous_position_getting_time = 1


    if mc_previous_rect_x< monster_rect.x:
        monster_rect.x -= MONSTER_VEL
    elif mc_previous_rect_x>  monster_rect.x:
        monster_rect.x+= MONSTER_VEL

    if mc_previous_rect_y>  monster_rect.y:
        monster_rect.y += MONSTER_VEL
    elif mc_previous_rect_y<  monster_rect.y:
        monster_rect.y-= MONSTER_VEL

    if abs(mc_previous_rect_x+30) > abs(monster_rect.x) and abs(mc_previous_rect_x-30) < abs(monster_rect.x) and abs(mc_previous_rect_y+30) > abs(monster_rect.y) and abs(mc_previous_rect_y-30) < abs(monster_rect.y):
        monster_helper_detection = False
        mc_previous_position_getting_time =0

    monster_chase_rotation_when_helped_by_monster(monster_rect,mc_previous_rect_x,mc_previous_rect_y)

def monster_chase_rotation_when_helped_by_monster(monster_rect,mc_previous_rect_x,mc_previous_rect_y):
    x_dist = abs(monster_rect.x)-abs(mc_previous_rect_x)
    y_dist = abs(monster_rect.y)-abs(mc_previous_rect_y)
    monster_rotation = math.degrees(math.atan2(x_dist,y_dist))
    monster_rotate = pygame.transform.rotate(MONSTER,monster_rotation)
    monster_center_rect = monster_rotate.get_rect(center = (monster_rect.x+MONSTER_WIDTH/2,monster_rect.y+MONSTER_HEIGHT/2))
    DISP.blit(monster_rotate,monster_center_rect)

def play_heart_beat_sound(monster_rect):
    if monster_rect.x >0 and monster_rect.x<WIDTH and monster_rect.y > 0 and monster_rect.y<HEIGHT and not monster_mc_collision:
        HEART_BEAT_SOUND.play()

def play_whistle_sound():
    helper_monster_decision = random.choice([1,2])
    if helper_monster_decision == 1:
        WHISTLE_SOUND_1.play()
    if helper_monster_decision == 2:
        WHISTLE_SOUND_2.play()

def collected_flesh_checker(mc_rect,flesh1_rect):
    global number_of_collected_flesh

    if  pygame.Rect.colliderect(mc_rect, flesh1_rect):
        number_of_collected_flesh = 1

    text = FONT.render(f'{number_of_collected_flesh}/1', True, RED)
    textRect = text.get_rect()
    textRect.center = (32,32)
    DISP.blit(text, textRect)

def flesh_initial_spawn(flesh1_rect,bottom_left_spawn_rect,top_right_spawn_rect):
    global flesh_initial_spawn_funcion_times

    if monster_initial_decision_to_spawn == 'b-l':
        flesh1_rect.x = bottom_left_spawn_rect.x
        flesh1_rect.y = bottom_left_spawn_rect.y

    if monster_initial_decision_to_spawn == 't-r':
        flesh1_rect.x = top_right_spawn_rect.x
        flesh1_rect.y = top_right_spawn_rect.y

    flesh_initial_spawn_funcion_times = 1

def main():
    
    global should_helper_monster_decision_continue
    global has_monster_helper_spawned

    bottom_left_spawn_rect = pygame.Rect(MONSTER_BORDER_LEFT_X+MONSTER_WIDTH+200,MONSTER_BORDER_DOWN_Y-MONSTER_HEIGHT-200,100,100)
    top_right_spawn_rect = pygame.Rect(MONSTER_BORDER_RIGHT_X-MONSTER_WIDTH-200,MONSTER_BORDER_UP_Y+MONSTER_HEIGHT+200,100,100)
    mc_rect = pygame.Rect(WIDTH/2-(WIDTH/6/2),HEIGHT/2-(HEIGHT/4/2),MC_WIDTH,MC_HEIGHT)

    flesh1_rect = pygame.Rect((WIDTH/2-(WIDTH/6/2),HEIGHT/2-(HEIGHT/4/2),FLESH_WIDTH,FLESH_HEIGHT))

    if monster_initial_decision_to_spawn == 'b-l':
        monster_rect = pygame.Rect(bottom_left_spawn_rect.x,bottom_left_spawn_rect.y,MONSTER_WIDTH,MONSTER_HEIGHT)
    if monster_initial_decision_to_spawn == 't-r':
        monster_rect = pygame.Rect(top_right_spawn_rect.x,top_right_spawn_rect.y,MONSTER_WIDTH,MONSTER_HEIGHT)

    background_rect = pygame.Rect(WIDTH/2-(BACKGROUND_WIDTH/2),HEIGHT/2-(BACKGROUND_HEIGHT/2),BACKGROUND_WIDTH,BACKGROUND_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or number_of_collected_flesh == 1:
                run = False

        draw_window()
        draw_mask_and_detection(monster_rect,mc_rect)
        game_border_and_draw_background(background_rect,flesh1_rect)
        move_characters(background_rect,monster_rect,flesh1_rect)

        if detected == True:
            chase(monster_rect,mc_rect)

        monsters_border(monster_rect)

        if not monster_mc_collision:
            draw_monster(monster_rect,mc_rect)

        if monster_helper_decision == False and detected == False:
            monster_mid_game_decision_to_spawn(monster_rect,bottom_left_spawn_rect,top_right_spawn_rect)


        if monster_helper_decision() and should_helper_monster_decision_continue:
            has_monster_helper_spawned = True
            should_helper_monster_decision_continue = False

            monster_helper_spawn_delay = threading.Timer(despawn_timer, despawn_monster_helper)
            monster_helper_spawn_delay.start()

        if has_monster_helper_spawned == True and not monster_mc_collision:
            draw_monster_helper(mc_rect)
            
        # draw_darkness(mc_rect)

        if flesh_initial_spawn_funcion_times ==0:
            flesh_initial_spawn(flesh1_rect,bottom_left_spawn_rect,top_right_spawn_rect)

        draw_characters(mc_rect)
        
        play_heart_beat_sound(monster_rect)

        # spawn point
        pygame.draw.rect(DISP,BLACK,bottom_left_spawn_rect)
        pygame.draw.rect(DISP,BLACK,top_right_spawn_rect)

        collected_flesh_checker(mc_rect,flesh1_rect)
        DISP.blit(FLESH,(flesh1_rect.x,flesh1_rect.y))
        if monster_mc_collision:
            bad_ending()
        pygame.display.update()
    pygame.quit()


def bad_ending():  # goood for me ^_^
    global monster_relief_musice_play_times
    BAD_ENDING_PIC_RECT = BAD_ENDING_SCALED_PIC.get_rect()
    if monster_relief_musice_play_times == 0:
        monster_relief.play(loops=1)
        monster_relief_musice_play_times = 1
    BAD_ENDING_PIC_RECT.center = (WIDTH/2,HEIGHT/2)
    DISP.blit(BAD_ENDING_SCALED_PIC,BAD_ENDING_PIC_RECT)

main()

def have_you_won():
    congrats_window = tk.Label(text="You won! and I don't care!")
    button = tk.Button(window, text='Ok', width=25, command=window.destroy)
    congrats_window.pack()
    button.pack()
    window.mainloop()

if number_of_collected_flesh == 1 and not monster_mc_collision:
    have_you_won()

if __name__ == '__Try_to_survive.py__':
    main()