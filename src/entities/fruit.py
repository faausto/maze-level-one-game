import pygame


class Fruit:
    def __init__(self, x, y, ancho=25, alto=25, tipo="", color=(255, 140, 0), puntos=10):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.tipo = tipo
        self.color = color
        self.puntos = puntos
        self.activa = True

    def recolectar(self):
        self.activa = False
        return self.puntos

    def esta_activa(self):
        return self.activa

    def get_rect(self):
        return self.rect
