import pygame

class Camara:
    def __init__(self, ancho_pantalla, alto_pantalla, ancho_mundo, alto_mundo):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.ancho_mundo = ancho_mundo
        self.alto_mundo = alto_mundo
        self.offset_x = 0
        self.offset_y = 0

    def actualizar(self, objetivo_rect):
        # calculamos el offset para centrar
        self.offset_x = objetivo_rect.centerx - self.ancho_pantalla // 2
        self.offset_y = objetivo_rect.centery - self.alto_pantalla // 2
        
        # aplicamos limites para que la camara no muestre fuera del mapa
        self.offset_x = max(0, min(self.offset_x, self.ancho_mundo - self.ancho_pantalla))
        self.offset_y = max(0, min(self.offset_y, self.alto_mundo - self.alto_pantalla))

    def aplicar_rect(self, rect):
        # devolvemos mundo ajustado por el offset
        return pygame.Rect(rect.x - self.offset_x, rect.y - self.offset_y, rect.w, rect.h)
