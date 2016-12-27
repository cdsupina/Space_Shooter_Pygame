import pygame
import random as rand
from sprites import *
from values import *

class Room():
    def __init__(self,room_type,enemy_number,connections):

        self.room_background_path = None
        self.room_code = None
        self.room_background = None
        self.enemy_number = enemy_number
        self.enemy_count = enemy_number
        self.enemy_sprite_group = pygame.sprite.Group()
        self.laser_sprite_group = pygame.sprite.Group()
        self.ally_sprite_group = pygame.sprite.Group()
        self.interactable_sprite_group = pygame.sprite.Group()
        self.enemies = []
        self.lasers = []
        self.portals = []
        self.portals_generated = False
        self.connections = connections

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




    def generate(self,screen):
        self.generate_room(screen)
        self.generate_enemies()

    def generate_room(self,screen):
        screen.blit(self.room_background,(0,0))

    def generate_enemies(self):

        i=0
        while i < self.enemy_number:
            enemy = Enemy(self,enemy_img_name,4,50,100+i*20,1)
            self.enemy_sprite_group.add(enemy)
            self.enemies.append(enemy)
            i += 1

    def generate_portals(self):
        for c in self.connections:
            loc = (100,100)
            if c == 0:
                loc = ((screen_width/2)-20,0)
            elif c == 1:
                loc = (screen_width-40,(screen_height/2)-20)
            elif c == 2:
                loc = ((screen_width/2)-20,screen_height-40)
            elif c == 3:
                loc = (0,(screen_height/2)-20)
            portal = Portal(self,portal_unexplored_img_names,90,loc[0],loc[1])
            self.interactable_sprite_group.add(portal)
            self.portals.append(portal)

    def generate_player_laser(self,player):
        new_laser = Player_Laser(self,player_laser_img_name,20,(player.rect.x+(player.width/2)-(5/2)),player.rect.y)
        self.laser_sprite_group.add(new_laser)
        self.lasers.append(new_laser)

    def draw_enemies(self,screen):
        self.enemy_sprite_group.draw(screen)

    def draw_lasers(self,screen):
        self.laser_sprite_group.draw(screen)

    def draw_allies(self,screen):
        self.ally_sprite_group.draw(screen)

    def draw_portals(self,screen,dt):
        for p in self.portals:
            p.animate(dt)

        self.interactable_sprite_group.draw(screen)

    def draw_all(self,screen,dt):
        self.generate_room(screen)
        self.draw_enemies(screen)

        if not self.portals_generated and self.enemy_count == 0:
            self.generate_portals()
            self.portals_generated = True
            self.draw_portals(screen,dt)
        elif self.portals_generated:
            self.draw_portals(screen,dt)

        self.draw_lasers(screen)
        self.draw_allies(screen)



    def __repr__(self):
        return "Background: " + self.room_background_path + " Room code: " + str(self.room_code)

'''
class Level():
    def __init__(self,room_count):

        self.room_count = room_count

'''        
