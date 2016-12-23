import pygame
from pygame.locals import *
from sys import exit
from sprites import *

clock = pygame.time.Clock()
fps = 60

SCREEN_SIZE = (640,480)
screen_height = SCREEN_SIZE[1]
screen_width = SCREEN_SIZE[0]

background_img_name = "assets/images/title_background.png"
scene_1_img_name = "assets/images/scene_1_background.png"
start_button_img_name = "assets/images/start_button.png"

ship_img_name = "assets/sprites/ship.png"

scene = 0

pygame.init()

#set up screen display and images
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
title_background = pygame.image.load(background_img_name).convert()
scene_1_background = pygame.image.load(scene_1_img_name).convert()
start_button = pygame.image.load(start_button_img_name).convert()

scene_1_sprite_group = pygame.sprite.Group()

ship = Ship(ship_img_name)
ship.rect.x = 100
ship.rect.y = 100

ship_x_change = 0
ship_y_change = 0

scene_1_sprite_group.add(ship)

while True:

    #scene rendering
    if scene == 0:
        screen.blit(title_background,(0,0))
        start = screen.blit(start_button,(220,300))


    elif scene == 1:
        screen.blit(scene_1_background,(0,0))
        scene_1_sprite_group.draw(screen)



    #listen for pygame events
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

        if event.type == KEYDOWN:
            if event.key == K_w:
                ship_y_change = -10
            if event.key == K_s:
                ship_y_change = 10
            if event.key == K_a:
                ship_x_change = -10
            if event.key == K_d:
                ship_x_change = 10
        if event.type == KEYUP:
            if event.key == K_w:
                ship_y_change = 0
            if event.key == K_s:
                ship_y_change = 0
            if event.key == K_a:
                ship_x_change = 0
            if event.key == K_d:
                ship_x_change = 0

    dt = clock.tick(fps)
    speed = float(dt)/64

    ship.rect.x += ship_x_change*speed
    ship.rect.y += ship_y_change*speed

    pygame.display.update()
