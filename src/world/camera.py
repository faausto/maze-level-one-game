"""Cámara que sigue al jugador dentro de un mundo más grande que la pantalla."""

import pygame

from src.constants import HUD_HEIGHT


class Camera:
    """Calcula el desplazamiento del mundo para mantener al jugador a la vista."""

    def __init__(self, ancho_mundo, alto_mundo, ancho_pantalla, alto_pantalla):
        self.ancho_mundo = ancho_mundo
        self.alto_mundo = alto_mundo
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.x = 0
        self.y = 0

    def update(self, jugador_rect):
        """Centra la cámara en el jugador sin salirse de los bordes del mundo."""
        self.x = jugador_rect.centerx - self.ancho_pantalla // 2
        self.y = jugador_rect.centery - (self.alto_pantalla - HUD_HEIGHT) // 2
        self.x = max(0, min(self.x, self.ancho_mundo - self.ancho_pantalla))
        self.y = max(0, min(self.y, self.alto_mundo - (self.alto_pantalla - HUD_HEIGHT)))

    def aplicar(self, rect):
        """Convierte un rectángulo del mundo a coordenadas de pantalla."""
        return pygame.Rect(
            rect.x - self.x,
            rect.y - self.y + HUD_HEIGHT,
            rect.width,
            rect.height,
        )
