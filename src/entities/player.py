import pygame


class Player:
    def __init__(self, x, y, ancho=40, alto=40):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.velocidad = 300

    def mover(self, dx, dy, maze, mundo_rect):
        nuevo_rect = self.rect.move(dx, 0)
        if not maze.colisiona(nuevo_rect):
            self.rect.x = nuevo_rect.x
        nuevo_rect = self.rect.move(0, dy)
        if not maze.colisiona(nuevo_rect):
            self.rect.y = nuevo_rect.y
        self.rect.clamp_ip(mundo_rect)

    def get_rect(self):
        return self.rect
