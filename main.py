import pygame
from pygame.locals import *
from sys import exit
from sprites import *
import random as rand

#setup frames per second
clock = pygame.time.Clock()
fps = 60

#setup the screen size
SCREEN_SIZE = (640,480)
screen_height = SCREEN_SIZE[1]
screen_width = SCREEN_SIZE[0]

#set variables equal to the locations of the image files
scene_0_background_img_names = ["assets/images/scene_0_background_1.png","assets/images/scene_0_background_2.png","assets/images/scene_0_background_3.png"]

title_img_name = "assets/images/title.png"
background_img_name = "assets/images/title_background.png"
scene_1_img_name = "assets/images/scene_1_background.png"
start_button_img_name = "assets/images/start_button.png"
quit_button_img_name = "assets/images/quit_button.png"
continue_button_img_name = "assets/images/continue_button.png"
pause_menu_img_name = "assets/images/pause_menu.png"
player_img_name = "assets/sprites/player_ship.png"
enemy_img_name = "assets/sprites/enemy_ship.png"
player_laser_img_name = "assets/sprites/player_blaster.png"

#set initial scene to 0
scene = 0

#start pygame
pygame.init()

#set up screen display and images
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)

#initialize images
scene_0_backgrounds = []
for s in scene_0_background_img_names:
    scene_0_backgrounds.append(pygame.image.load(s).convert())

title = pygame.image.load(title_img_name).convert_alpha()
title_background = pygame.image.load(background_img_name).convert()
scene_1_background = pygame.image.load(scene_1_img_name).convert()
start_button = pygame.image.load(start_button_img_name).convert()
quit_button = pygame.image.load(quit_button_img_name).convert()
continue_button = pygame.image.load(continue_button_img_name).convert()
pause_menu = pygame.image.load(pause_menu_img_name).convert_alpha()


player = Ship(player_img_name,10)
player.rect.x = 100
player.rect.y = 100

player_x_change = 0
player_y_change = 0

#enemy_1 = Enemy(enemy_img_name,4,50,200,200)


scene_1_sprite_group = pygame.sprite.Group()
scene_1_sprite_group.add(player)
#scene_1_sprite_group.add(enemy_1)

#setup a paused state
paused = False

lasers = []
enemies = []
#enemies.append(enemy_1)

scene_0_background_idx = 0
scene_0_background_animation_time = 150
scene_0_current_animation_time = 100
while True:

    dt = clock.tick(fps)
    speed = float(dt)/64

    ##########SCENE-RENDERING#########
    if scene == 0:



        if scene_0_current_animation_time >= scene_0_background_animation_time:

            scene_0_current_animation_time = 0
            screen.blit(scene_0_backgrounds[scene_0_background_idx],(0,0))
            screen.blit(title,(0,0))
            scene_0_background_idx += 1
        else:
            scene_0_current_animation_time += dt

        if scene_0_background_idx > 2:
            scene_0_background_idx = 0


        start = screen.blit(start_button,(220,200))
        quit = screen.blit(quit_button,(220,300))


    elif scene == 1:
        screen.blit(scene_1_background,(0,0))
        scene_1_sprite_group.draw(screen)
        if paused:
            screen.blit(pause_menu,(160,120))
            quit = screen.blit(quit_button,(220,266))
            continue_but = screen.blit(continue_button,(220,193))
        elif not paused:
            for l in lasers:
                l.rect.y += -l.speed*speed
                l.time_spawned += dt
                if l.time_spawned >= 1000:
                    scene_1_sprite_group.remove(l)
                    lasers.remove(l)
                    #l = None
                for e in enemies:
                    if l.rect.colliderect(e.rect):
                        scene_1_sprite_group.remove(l)
                        scene_1_sprite_group.remove(e)
                        lasers.remove(l)
                        enemies.remove(e)
                        #l = None

            for e in enemies:

                e.current_displacement = abs(e.loc_init[0]-e.rect.x)

                #print(e.current_displacement)
                if e.current_displacement>=e.max_displacement:
                    e.speed = -e.speed

                e.rect.x += e.speed*speed
                if e.rect.x >= (e.loc_init[0]+e.max_displacement):
                    e.rect.x = e.loc_init[0]+e.max_displacement
                elif e.rect.x <= (e.loc_init[0]-e.max_displacement):
                    e.rect.x = e.loc_init[0]-e.max_displacement
            player.rect.x += player_x_change*speed
            player.rect.y += player_y_change*speed






    ##########EVENT-LISTENING##########
    for event in pygame.event.get():
        #print the events
        print(event)
        if event.type == QUIT:
            exit()

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if scene == 0:
                    if start.collidepoint(pygame.mouse.get_pos()):
                        scene = 1
                        enemy_count = rand.randint(10,15)
                        i = 0
                        while i< enemy_count:
                            enemy = Enemy(enemy_img_name,4,50,100+i*20,200)
                            scene_1_sprite_group.add(enemy)
                            enemies.append(enemy)
                            i += 1

                    if quit.collidepoint(pygame.mouse.get_pos()):
                        exit()
                if scene == 1:
                    if paused:
                        if continue_but.collidepoint(pygame.mouse.get_pos()):
                            paused = False
                        if quit.collidepoint(pygame.mouse.get_pos()):
                            exit()

        if event.type == KEYDOWN:
            if not paused:
                if event.key == K_w:
                    player_y_change = -player.speed
                elif event.key == K_s:
                    player_y_change = player.speed
                elif event.key == K_a:
                    player_x_change = -player.speed
                elif event.key == K_d:
                    player_x_change = player.speed
                elif event.key == K_SPACE:
                        new_laser = Player_Laser(player_laser_img_name,20,(player.rect.x+(player.width/2)-(5/2)),player.rect.y)
                        scene_1_sprite_group.add(new_laser)
                        lasers.append(new_laser)

                        print(lasers)

        if event.type == KEYUP:
            if event.key == K_w:
                player_y_change = 0
            elif event.key == K_s:
                player_y_change = 0
            elif event.key == K_a:
                player_x_change = 0
            elif event.key == K_d:
                player_x_change = 0
            if event.key == K_ESCAPE:
                if not paused:
                    paused = True
                elif paused:
                    paused = False



    pygame.display.update()
