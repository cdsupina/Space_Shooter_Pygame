import pygame
from pygame.locals import *
from sys import exit
from sprites import *
import random as rand
from values import *
from levels import *
from splash_screens import *
import math

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
map_bg = pygame.image.load(map_overlay_img).convert_alpha()

#rooms
unexplored_room = pygame.image.load(unexplored_room_img).convert_alpha()
explored_room = pygame.image.load(explored_room_img).convert_alpha()
starting_room = pygame.image.load(starting_room_img).convert_alpha()
boss_room = pygame.image.load(boss_room_img).convert_alpha()

#initialize the player
player = Ship(player_img_name,10,100,100)

#set paused status to false
paused = False
map_showing = False
#initialize first room

size = 5

#level_1 = Level([(2,0),(4,0,"x"),(0,1),(2,1),(4,1),(0,2),(1,2),(2,2,"*"),(3,2),(4,2),(2,3),(2,4)])
level_1 = Level(size)
#add the player to the allies sprite group
#print(level_1.current_room)
level_1.current_room.ally_sprite_group.add(player)

scene_0_images = [(title,(0,0))]
scene_0_buttons = [(start_button,(220,200)),(quit_button,(220,300))]
title_screen = Splash_Screen((0,0),150,scene_0_backgrounds,scene_0_images,scene_0_buttons)

pause_menu_backgrounds = [pause_menu]
pause_menu_images = []
pause_menu_buttons = [(continue_button,(220,193)),(quit_button,(220,266))]
pause_menu = Splash_Screen((160,120),0,pause_menu_backgrounds,pause_menu_images,pause_menu_buttons)

map_overlay_backgrounds = [map_bg]
map_overlay = Splash_Screen((0,0),0,map_overlay_backgrounds,[(starting_room,(305,225))],[])


while True:

    #set clock to save the time between frames
    dt = clock.tick(fps)
    speed = float(dt)/64

    ##########SCENE-RENDERING#########
    #rendering for title scene
    if scene == 0:
        title_screen.display(screen,dt)

    #rendering for the firsl level scene
    elif scene == 1:
        level_1.current_room.draw_all(screen,dt)

        if paused:
            pause_menu.display(screen,dt)

        elif not paused:

            #print(level_1.current_room)

            for l in level_1.current_room.lasers:
                l.behave(speed,dt)
                for e in level_1.current_room.enemies:
                    l.on_collision(e)

            for e in level_1.current_room.enemies:
                e.behave(speed)

            for p in level_1.current_room.portals:
                p.on_collision(player,screen)


            player.behave(speed)

        if map_showing:
            map_overlay.display(screen,dt)

    ##########EVENT-LISTENING##########
    for event in pygame.event.get():
        #print the events
        #print(event)
        if event.type == QUIT:
            exit()

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if scene == 0:
                    if title_screen.buttons[0].collidepoint(pygame.mouse.get_pos()):
                        scene = 1
                        level_1.current_room.generate(screen)

                    if title_screen.buttons[1].collidepoint(pygame.mouse.get_pos()):
                        exit()
                if scene == 1:
                    if paused:
                        if pause_menu.buttons[0].collidepoint(pygame.mouse.get_pos()):
                            paused = False
                        if pause_menu.buttons[1].collidepoint(pygame.mouse.get_pos()):
                            exit()

        if event.type == KEYDOWN:
            if not paused:
                if event.key == K_w:
                    player.accelerate(0)
                elif event.key == K_s:
                    player.accelerate(1)
                elif event.key == K_a:
                    player.accelerate(2)
                elif event.key == K_d:
                    player.accelerate(3)
                elif event.key == K_SPACE:
                    level_1.current_room.generate_player_laser(player)

        if event.type == KEYUP:
            if event.key == K_w:
                player.deccelerate(0)
            elif event.key == K_s:
                player.deccelerate(1)
            elif event.key == K_a:
                player.deccelerate(2)
            elif event.key == K_d:
                player.deccelerate(3)
            if event.key == K_ESCAPE:
                if not paused:
                    paused = True
                elif paused:
                    paused = False
            if event.key == K_m:
                if not map_showing:
                    map_showing = True
                elif map_showing:
                    map_showing = False

    pygame.display.update()
