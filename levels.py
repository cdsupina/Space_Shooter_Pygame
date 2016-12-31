import pygame
import random as rand
from sprites import *
from values import *

class Room():
    def __init__(self,level,room_type,enemy_number):

        self.room_type = room_type
        self.room_background_path = self.generate_room_background_path()
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
        self.connections = [0,1,2,3]
        self.level = level
        self.room_background = pygame.image.load(self.room_background_path).convert()


    def generate_room_background_path(self):
        result = None
        if self.room_type == 0:
            result = scene_1_start_room
        elif self.room_type == 2:
            result = scene_1_boss_room
        else:
            result = scene_1_img_name
        return result

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
            portal = Portal(self,self.level,portal_unexplored_img_names,90,loc[0],loc[1])
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
            self.enemy_number = 0
            self.generate_portals()
            self.portals_generated = True
            self.draw_portals(screen,dt)
        elif self.portals_generated:
            self.draw_portals(screen,dt)

        self.draw_lasers(screen)
        self.draw_allies(screen)



    def __repr__(self):
        return str(self.room_type)+ " " + str(self.connections) + " " + str(self.level.current_room_coor)


class Level():
    def __init__(self,locs):

        self.current_room_coor = None
        self.level_map = []
        self.locs = locs
        self.current_room = None
        self.generate_map()
        #self.current_room = self.rooms[0]




    def generate_map(self):
        coor = (None,None)


        #generate map layout
        for y in range(5):
            new_row = []

            for x in range(5):
                coor = (x,y)
                added = False
                for l in self.locs:
                    if l[0] == coor[0] and l[1] == coor[1]:
                        if len(l) > 2:
                            if l[2] == "*":
                                self.current_room = Room(self,0,0)
                                self.current_room_coor = [coor[0],coor[1]]
                                new_row.append(self.current_room)
                                self.locs.remove(l)
                                added = True
                            elif l[2] == "x":
                                new_row.append(Room(self,2,1))
                                self.locs.remove(l)
                                added = True
                        else:
                            new_row.append(Room(self,1,rand.randint(1,3)))
                            self.locs.remove(l)
                            added = True
                if not added:
                    new_row.append(None)

            self.level_map.append(new_row)

        #generate connections
        current_x = 0
        current_y = 0
        for y in self.level_map:

            for x in y:
                #print("coor: " + str(current_x) + "," + str(current_y))
                if x != None:
                    #generate top portal
                    if current_y == 0:
                        x.connections.remove(0)


                    elif current_y > 0:
                        if self.level_map[current_y-1][current_x] == None:
                            x.connections.remove(0)

                    #generate right portal
                    if current_x == len(y)-1:
                        x.connections.remove(1)
                    elif current_x < len(y)-1:
                        if self.level_map[current_y][current_x+1] == None:
                            x.connections.remove(1)

                    #generate bottom portal
                    if current_y == len(self.level_map)-1:
                        x.connections.remove(2)
                    elif current_y < len(self.level_map)-1:
                        if self.level_map[current_y+1][current_x] == None:
                            x.connections.remove(2)

                    #generate left portal
                    if current_x == 0:
                        x.connections.remove(3)
                    elif current_x > 0:
                        if self.level_map[current_y][current_x-1] == None:
                            x.connections.remove(3)


                current_x += 1
            current_x = 0
            current_y += 1
        #print(self.level_map)
