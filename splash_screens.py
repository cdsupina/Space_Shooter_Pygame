import pygame

class Splash_Screen():
    def __init__(self,loc,ani_time,frames,images,button_info):
        self.background_ani_idx = 0
        self.ani_time = ani_time
        self.current_ani_time = ani_time
        self.frames = frames
        self.images = images
        self.loc = loc
        self.button_info = button_info
        self.buttons = []

    def display(self,screen,dt):
        if self.ani_time > 0:

            if self.current_ani_time >= self.ani_time:
                self.current_ani_time = 0
                screen.blit(self.frames[self.background_ani_idx],self.loc)
                self.display_buttons(screen)
                for i in self.images:
                    screen.blit(i[0],i[1])

                self.background_ani_idx += 1
            else:
                self.current_ani_time += dt

            if self.background_ani_idx >= len(self.frames):
                self.background_ani_idx = 0

        else:
            screen.blit(self.frames[0],self.loc)
            self.display_buttons(screen)

    def display_buttons(self,screen):
        for b in self.button_info:
            self.buttons.append(screen.blit(b[0],b[1]))
