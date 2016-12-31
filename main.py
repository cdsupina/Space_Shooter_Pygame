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

#initialize the player
player = Ship(player_img_name,10,100,100)

#set paused status to false
paused = False

#initialize first room

size = 5
spaces = size*size
room_count = spaces//2
center = (size//2,size//2)
floor_map = []
coors = []
#first run through, generate map full of coordinates, marking the center coordinate appropriatly
for row in range(size):
    new_row = []
    for col in range(size):
        current_coor = (col,row)
        if current_coor == (center):
            new_row.append((col,row,"*"))
            coors.append((col,row,"*"))
        elif current_coor == (center[0]+1,center[1]) or current_coor == (center[0]-1,center[1]) or current_coor == (center[0],center[1]+1) or current_coor == (center[0],center[1]-1):
            new_row.append((col,row))
            coors.append((col,row))
        else:
            new_row.append(None)
    floor_map.append(new_row)

#generate rest of rooms
#print(coors)
coors_generated = 5

while coors_generated < room_count:

    y=0
    for row in floor_map:
        room_gen = rand.randint(0,size-1)
        if row[room_gen] == None and coors_generated < room_count:
            coor_candidate = (room_gen,y)
            coor_added = False
            for coor in coors:
                if coor_candidate[1] == coor[1] and coor_candidate[0] == coor[0]+1 or coor_candidate[1] == coor[1] and coor_candidate[0] == coor[0]-1 or coor_candidate[0] == coor[0] and coor_candidate[1] == coor[1]+1 or coor_candidate[0] == coor[0] and coor_candidate[1] == coor[1]-1:
                    coors_generated += 1
                    coors.append(coor_candidate)
                    coor_added = True
                    row[room_gen] = coor_candidate
                    #print(coors)
                if coor_added:
                    break
        #print(floor_map)
        y += 1

#generate the boss room

#find rooms that are the furthest from the starting room
max_dist = 0
boss_candidates = []
for coor in coors:
    dist = abs(coor[0]-center[0]) + abs(coor[1]-center[1])
    #print(str(coor) + " " + str(dist))
    if dist > max_dist:
        max_dist = dist

#add rooms with the maximum distance to the list of candidates
for coor in coors:
    if abs(coor[0]-center[0]) + abs(coor[1]-center[1]) == max_dist:
        boss_candidates.append(coor)

#choose a candidate
boss_room = boss_candidates[rand.randint(0,len(boss_candidates)-1)]

for coor in coors:
    if boss_room == coor:
        new_coor = (coor[0],coor[1],"x")
        coors.remove(coor)
        coors.append(new_coor)
        break

print(boss_candidates)
print(boss_room)
for row in floor_map:
    print(row)
#level_1 = Level([(2,0),(4,0,"x"),(0,1),(2,1),(4,1),(0,2),(1,2),(2,2,"*"),(3,2),(4,2),(2,3),(2,4)])
level_1 = Level(coors)
#add the player to the allies sprite group
level_1.current_room.ally_sprite_group.add(player)

scene_0_images = [(title,(0,0))]
scene_0_buttons = [(start_button,(220,200)),(quit_button,(220,300))]
title_screen = Splash_Screen((0,0),150,scene_0_backgrounds,scene_0_images,scene_0_buttons)

pause_menu_backgrounds = [pause_menu]
pause_menu_images = []
pause_menu_buttons = [(continue_button,(220,193)),(quit_button,(220,266))]
pause_menu = Splash_Screen((160,120),0,pause_menu_backgrounds,pause_menu_images,pause_menu_buttons)

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

    pygame.display.update()
