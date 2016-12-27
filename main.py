import pygame
from pygame.locals import *
from sys import exit
from sprites import *
import random as rand
from values import *
from rooms import *

#setup frames per second
clock = pygame.time.Clock()

#set initial scene to 0
scene = 0

#start pygame
pygame.init()

#set up screen display and images
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)

#initialize all images
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

#initialize the player
player = Ship(player_img_name,10,100,100)

#set paused status to false
paused = False

#set up title screen animation
scene_0_background_idx = 0
scene_0_background_animation_time = 150
scene_0_current_animation_time = 100

#initialize first room
room_1 = Room(1,20)

#add the player to the allies sprite group
room_1.ally_sprite_group.add(player)

while True:

    #set clock to save the time between frames
    dt = clock.tick(fps)
    speed = float(dt)/64

    ##########SCENE-RENDERING#########

    #rendering for title scene
    if scene == 0:
        #animate background for title screen
        if scene_0_current_animation_time >= scene_0_background_animation_time:

            scene_0_current_animation_time = 0
            screen.blit(scene_0_backgrounds[scene_0_background_idx],(0,0))
            screen.blit(title,(0,0))
            start = screen.blit(start_button,(220,200))
            quit = screen.blit(quit_button,(220,300))
            scene_0_background_idx += 1
        else:
            scene_0_current_animation_time += dt

        if scene_0_background_idx > 2:
            scene_0_background_idx = 0

    #rendering for the firsl level scene
    elif scene == 1:
        room_1.draw_all(screen)
        if paused:
            screen.blit(pause_menu,(160,120))
            quit = screen.blit(quit_button,(220,266))
            continue_but = screen.blit(continue_button,(220,193))
        elif not paused:
            for l in room_1.lasers:
                l.rect.y += -l.speed*speed
                l.time_spawned += dt
                if l.time_spawned >= 1000:
                    room_1.laser_sprite_group.remove(l)
                    room_1.lasers.remove(l)
                for e in room_1.enemies:
                    if l.rect.colliderect(e.rect):
                        room_1.laser_sprite_group.remove(l)
                        room_1.enemy_sprite_group.remove(e)
                        room_1.lasers.remove(l)
                        room_1.enemies.remove(e)

            for e in room_1.enemies:
                e.behave(speed)

            player.rect.x += player.x_change*speed
            player.rect.y += player.y_change*speed


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
                        room_1.generate(screen)

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
                    player.y_change = -player.speed
                elif event.key == K_s:
                    player.y_change = player.speed
                elif event.key == K_a:
                    player.x_change = -player.speed
                elif event.key == K_d:
                    player.x_change = player.speed
                elif event.key == K_SPACE:
                    room_1.generate_player_laser(player)

        if event.type == KEYUP:
            if event.key == K_w:
                player.y_change = 0
            elif event.key == K_s:
                player.y_change = 0
            elif event.key == K_a:
                player.x_change = 0
            elif event.key == K_d:
                player.x_change = 0
            if event.key == K_ESCAPE:
                if not paused:
                    paused = True
                elif paused:
                    paused = False



    pygame.display.update()
