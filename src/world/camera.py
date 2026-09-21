import pygame


class Camera:
    def __init__(self, ancho_mundo, alto_mundo, ancho_pantalla, alto_pantalla):
        self.ancho_mundo = ancho_mundo
        self.alto_mundo = alto_mundo
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.x = 0
        self.y = 0

    def update(self, jugador_rect):
        self.x = jugador_rect.centerx - self.ancho_pantalla // 2
        self.y = jugador_rect.centery - self.alto_pantalla // 2
        self.x = max(0, min(self.x, self.ancho_mundo - self.ancho_pantalla))
        self.y = max(0, min(self.y, self.alto_mundo - self.alto_pantalla))

    def aplicar(self, rect):
        return pygame.Rect(rect.x - self.x, rect.y - self.y, rect.width, rect.height)
