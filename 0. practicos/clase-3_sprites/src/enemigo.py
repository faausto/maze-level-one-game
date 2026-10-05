import pygame
import random


class Enemigo(pygame.sprite.Sprite):
    def __init__(self, pantalla_rect):
        super().__init__()
        self.image = pygame.image.load("assets/images/alien.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, pantalla_rect.width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidad = random.randint(100, 250)
        self.pantalla_rect = pantalla_rect

    def update(self, dt, *args):
        self.rect.y += self.velocidad * dt
        if self.rect.top > self.pantalla_rect.bottom:
            self.kill()