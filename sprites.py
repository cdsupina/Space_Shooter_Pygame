import pygame
from values import *

class Ship(pygame.sprite.Sprite):
    def __init__(self,image,speed,init_x,init_y):
        super().__init__()

        self.speed = speed
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = init_x
        self.rect.y = init_y
        self.x_change = 0
        self.y_change = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,speed,displacement,init_x,init_y):
        super().__init__()

        self.x_speed = speed
        self.y_speed = speed
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.max_displacement = displacement
        self.current_displacement = 0
        self.rect.x = init_x
        self.rect.y = init_y
        self.loc_init = (self.rect.x,self.rect.y)



    def behave(self,speed):
        self.current_displacement = abs(self.loc_init[0]-self.rect.x)

        if self.current_displacement>=self.max_displacement:
            self.x_speed = -self.x_speed

        if self.rect.y >= screen_height - self.image.get_height() or self.rect.y <= 0:
            self.y_speed = -self.y_speed

        self.rect.x += self.x_speed*speed
        self.rect.y += self.y_speed*speed

        if self.rect.x >= (self.loc_init[0]+self.max_displacement):
            self.rect.x = self.loc_init[0]+self.max_displacement
        elif self.rect.x <= (self.loc_init[0]-self.max_displacement):
            self.rect.x = self.loc_init[0]-self.max_displacement

class Player_Laser(pygame.sprite.Sprite):
    def __init__(self,image,speed,x,y):
        super().__init__()

        self.speed = speed
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.time_spawned = 0

    def __repr__(self):
        return "X coor: " + str(self.rect.x) + " Y coor: " + str(self.rect.y) + " Time: " + str(self.time_spawned)
