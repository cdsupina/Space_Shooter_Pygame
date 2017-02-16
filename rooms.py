import pygame
import random as rand
from sprites import *
from values import *

'''
class: room to make up levels
    room_type: integer representing the type of room
    enemy_number: number of enemies to be spawned in the room
'''
class Room():
    def __init__(self,room_type,enemy_number):

        self.room_background_path = None
        self.room_code = None
        self.room_background = None
        self.enemy_number = enemy_number
        self.enemy_sprite_group = pygame.sprite.Group()
        self.laser_sprite_group = pygame.sprite.Group()
        self.ally_sprite_group = pygame.sprite.Group()
        self.enemies = []
        self.lasers = []

        if room_type == 0:
            self.room_background_path = scene_1_start_room
        else:
            self.room_background_path = scene_1_img_name

        if room_type != 0:
            if enemy_number == 1:
                self.room_code = rand.randint(0,1)
            if enemy_number == 2:
                self.room_code = rand.randint(2,3)

        self.room_background = pygame.image.load(self.room_background_path).convert()

    '''
    function: full room and everything in it
        screen: pygame display to display the room on
    '''
    def generate(self,screen):
        self.generate_room(screen)
        self.generate_enemies()

    '''
    function: generates the room on the screen
        screen: pygame display to display the room on
    '''
    def generate_room(self,screen):
        screen.blit(self.room_background,(0,0))

    '''
    function: generate the enemies to occupy the room
    '''
    def generate_enemies(self):

        i=0
        while i < self.enemy_number:
            enemy = Enemy(self,enemy_img_name,4,50,100+i*20,1)
            self.enemy_sprite_group.add(enemy)
            self.enemies.append(enemy)
            i += 1

    '''
    function: generate the lasers to occupy the room
        player: player object to generate the laser for
    '''
    def generate_player_laser(self,player):
        new_laser = Player_Laser(self,player_laser_img_name,20,(player.rect.x+(player.width/2)-(5/2)),player.rect.y)
        self.laser_sprite_group.add(new_laser)
        self.lasers.append(new_laser)

    '''
    function: draw the enemies on the screen
        screen: pygame display to draw the enemies on
    '''
    def draw_enemies(self,screen):
        self.enemy_sprite_group.draw(screen)

    '''
    function: draw the lasers on the screen
        screen: pygame display to draw the lasers on
    '''
    def draw_lasers(self,screen):
        self.laser_sprite_group.draw(screen)

    '''
    function: draw the allies on the screen
        screen: pygame display to draw the allies on
    '''
    def draw_allies(self,screen):
        self.ally_sprite_group.draw(screen)

    '''
    function: draw everything on the screen
        screen: pygame display to draw on
    '''
    def draw_all(self,screen):
        self.generate_room(screen)
        self.draw_enemies(screen)
        self.draw_lasers(screen)
        self.draw_allies(screen)


    def __repr__(self):
        return "Background: " + self.room_background_path + " Room code: " + str(self.room_code)
