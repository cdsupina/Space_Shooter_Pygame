import pygame
from values import *

'''
class: controllable player
    image: path to the image for the sprite
    speed: speed of the player
    init_x: initial x coordinate of the player
    init_y: initial y coordinate of the player
'''
class Player(pygame.sprite.Sprite):
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

    '''
    function: behave by  adjusting the values
        speed: float speed of the game
    '''
    def behave(self,speed):
        self.rect.x += self.x_change*speed
        self.rect.y += self.y_change*speed

        if self.rect.x >= SCREEN_WIDTH-20:
            self.rect.x = SCREEN_WIDTH-20
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= SCREEN_HEIGHT-20:
            self.rect.y = SCREEN_HEIGHT-20
        if self.rect.y <= 0:
            self.rect.y = 0

    '''
    function: adjust x_change or y_change
        direction: integer 0 through 3 representing different directions
    '''
    def accelerate(self,direction):
        if direction == 0:
            self.y_change = -self.speed
        if direction == 1:
            self.y_change = self.speed
        if direction == 2:
            self.x_change = -self.speed
        if direction == 3:
            self.x_change = self.speed

    '''
    function: set x_change or y_change to 0
        direction: integer 0 through 3 representing different directions
    '''
    def deccelerate(self,direction):
        if direction == 0:
            self.y_change = 0
        if direction == 1:
            self.y_change = 0
        if direction == 2:
            self.x_change = 0
        if direction == 3:
            self.x_change = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self,room,image,speed,displacement,init_x,init_y):
        super().__init__()

        self.room = room
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

        if self.rect.y >= SCREEN_HEIGHT - self.image.get_height() or self.rect.y <= 0:
            self.y_speed = -self.y_speed

        self.rect.x += self.x_speed*speed
        self.rect.y += self.y_speed*speed

        if self.rect.x >= (self.loc_init[0]+self.max_displacement):
            self.rect.x = self.loc_init[0]+self.max_displacement
        elif self.rect.x <= (self.loc_init[0]-self.max_displacement):
            self.rect.x = self.loc_init[0]-self.max_displacement

class Player_Laser(pygame.sprite.Sprite):
    def __init__(self,room,image,speed,x,y):
        super().__init__()

        self.room = room
        self.speed = speed
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.time_spawned = 0

    def behave(self,speed,dt):
        self.rect.y += -self.speed*speed
        self.time_spawned += dt
        if self.time_spawned >= 1000:
            self.room.laser_sprite_group.remove(self)
            self.room.lasers.remove(self)

    def on_collision(self,enemy):
        if self.rect.colliderect(enemy.rect):
            self.room.laser_sprite_group.remove(self)
            self.room.enemy_sprite_group.remove(enemy)
            self.room.lasers.remove(self)
            self.room.enemies.remove(enemy)
            self.room.enemy_count -= 1

    def __repr__(self):
        return "X coor: " + str(self.rect.x) + " Y coor: " + str(self.rect.y) + " Time: " + str(self.time_spawned)

class Portal(pygame.sprite.Sprite):
    def __init__(self,room,level,frames,ani_time,x,y):
        super().__init__()

        self.room = room
        self.frames = frames
        self.current_frame = frames[0]
        self.image = pygame.image.load(self.current_frame)
        self.frame_idx = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ani_time = ani_time
        self.current_ani_time = ani_time
        self.level = level

    def animate(self,dt):
        if self.current_ani_time >= self.ani_time:
            self.current_ani_time = 0
            self.image = pygame.image.load(self.current_frame)

            self.frame_idx += 1
            if self.frame_idx >= len(self.frames):
                self.frame_idx = 0
            self.current_frame = self.frames[self.frame_idx]
        else:
            self.current_ani_time += dt

    def on_collision(self,player,screen):
        if self.rect.colliderect(player.rect):
            #print("portal touching player")
            if self.rect.x == (SCREEN_WIDTH/2)-20 and self.rect.y == 0:
                #print("top portal touching player")
                self.level.current_room_coor[1] -= 1
                self.level.current_room = self.level.level_map[self.level.current_room_coor[1]][self.level.current_room_coor[0]]
                self.level.current_room.generate(screen)
                self.level.current_room.ally_sprite_group.add(player)
                player.rect.x = (SCREEN_WIDTH/2)-10
                player.rect.y = SCREEN_HEIGHT - 60

            if self.rect.x == SCREEN_WIDTH-40 and self.rect.y == (SCREEN_HEIGHT/2)-20:
                #print("right portal touching player")
                self.level.current_room_coor[0] += 1
                self.level.current_room = self.level.level_map[self.level.current_room_coor[1]][self.level.current_room_coor[0]]
                self.level.current_room.generate(screen)
                self.level.current_room.ally_sprite_group.add(player)
                player.rect.x = 60
                player.rect.y = (SCREEN_HEIGHT/2)-10

            if self.rect.x == (SCREEN_WIDTH/2)-20 and self.rect.y == SCREEN_HEIGHT-40:
                #print("bottom portal touching player")
                self.level.current_room_coor[1] += 1
                self.level.current_room = self.level.level_map[self.level.current_room_coor[1]][self.level.current_room_coor[0]]
                self.level.current_room.generate(screen)
                self.level.current_room.ally_sprite_group.add(player)
                player.rect.x = (SCREEN_WIDTH/2)-10
                player.rect.y = 60

            if self.rect.x == 0 and self.rect.y == (SCREEN_HEIGHT/2)-20:
                #print("left portal touching player")
                self.level.current_room_coor[0] -= 1
                self.level.current_room = self.level.level_map[self.level.current_room_coor[1]][self.level.current_room_coor[0]]
                self.level.current_room.generate(screen)
                self.level.current_room.ally_sprite_group.add(player)
                player.rect.x = SCREEN_WIDTH - 60
                player.rect.y = (SCREEN_HEIGHT/2)-10
