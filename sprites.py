import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()

        self.image = pygame.image.load(image)

        self.rect = self.image.get_rect()
