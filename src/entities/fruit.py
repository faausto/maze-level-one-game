"""Entidad de las frutas coleccionables."""

import logging
import random

import pygame

from src.constants import IMAGES_DIR

logger = logging.getLogger(__name__)


class Fruit:
    """Fruta que otorga puntos al recolectarla."""

    _sprite_sheet = None
    _frames = None
    _frame_size = 32
    _draw_size = _frame_size + 6

    def __init__(self, x, y, ancho=32, alto=32, tipo="", color=(255, 140, 0), puntos=10):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.tipo = tipo
        self.color = color
        self.puntos = puntos
        self.activa = True
        self.start_time = pygame.time.get_ticks()
        self.float_offset = random.uniform(0, 6.28)
        self.frame_index = random.randint(0, 23)

        if Fruit._frames is None:
            self._load_sprites()

    @classmethod
    def _load_sprites(cls):
        try:
            sheet = pygame.image.load(
                IMAGES_DIR / "fruits" / "fruits.png"
            ).convert_alpha()
            cls._sprite_sheet = sheet
            cls._frames = []
            cols = 5
            rows = 5
            tamano = (cls._draw_size, cls._draw_size)
            for row in range(rows):
                for col in range(cols):
                    if row == rows - 1 and col == cols - 1:
                        continue
                    x = col * cls._frame_size
                    y = row * cls._frame_size
                    frame = sheet.subsurface(
                        pygame.Rect(x, y, cls._frame_size, cls._frame_size)
                    )
                    cls._frames.append(pygame.transform.scale(frame, tamano))
        except (pygame.error, OSError) as error:
            logger.warning("No se pudieron cargar los sprites de frutas: %s", error)
            cls._frames = []

    def recolectar(self):
        """Marca la fruta como recolectada y devuelve sus puntos."""
        self.activa = False
        return self.puntos

    def get_sprite(self):
        """Devuelve el frame actual ya escalado."""
        if Fruit._frames and 0 <= self.frame_index < len(Fruit._frames):
            return Fruit._frames[self.frame_index]
        return None

    def get_float_offset(self):
        """Desplazamiento vertical suave para el efecto de flotación."""
        t = (pygame.time.get_ticks() - self.start_time) / 1000.0
        return int(
            3 * pygame.math.Vector2(1, 0).rotate(t * 240 + self.float_offset).y
        )
