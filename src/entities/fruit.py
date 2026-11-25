"""Entidad de las frutas coleccionables."""

import logging
import random
from typing import ClassVar

import pygame

from src.constants import IMAGES_DIR, TAMANIO_FRUTA

logger = logging.getLogger(__name__)

# Mapea el tipo de fruta (en español, como se usa en seeds) al archivo de imagen.
SPRITES_POR_TIPO = {
    "manzana": "apple.png",
    "banana": "banana.png",
    "uva": "grape.png",
    "naranja": "orange.png",
    "pera": "pear.png",
    "frutilla": "strawberry.png",
    "melon": "melon.png",
    "durazno": "peach.png",
    "cereza": "cherry.png",
    "pina": "pineapple.png",
    "limon": "lemon.png",
    "mandarina": "tangerine.png",
}


class Fruit:
    """Fruta que otorga puntos al recolectarla."""

    _sprites: ClassVar[dict] = {}
    _cargados: ClassVar[set] = set()

    def __init__(
        self,
        x,
        y,
        ancho=TAMANIO_FRUTA,
        alto=TAMANIO_FRUTA,
        tipo="",
        color=(255, 140, 0),
        puntos=10,
    ):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.tipo = tipo
        self.color = color
        self.puntos = puntos
        self.activa = True
        self.start_time = pygame.time.get_ticks()
        self.float_offset = random.uniform(0, 6.28)

        self._cargar_sprite_tipo(tipo)

    @classmethod
    def _cargar_sprite_tipo(cls, tipo):
        """Carga y cachea el sprite individual del tipo de fruta."""
        if tipo in cls._cargados:
            return
        cls._cargados.add(tipo)

        nombre_archivo = SPRITES_POR_TIPO.get(tipo)
        if not nombre_archivo:
            cls._sprites[tipo] = None
            return

        ruta = IMAGES_DIR / "fruits" / nombre_archivo
        try:
            imagen = pygame.image.load(ruta).convert_alpha()
            if imagen.get_size() != (cls._ancho(), cls._alto()):
                imagen = pygame.transform.scale(
                    imagen, (cls._ancho(), cls._alto())
                )
            cls._sprites[tipo] = imagen
        except (pygame.error, OSError) as error:
            logger.warning("No se pudo cargar el sprite de fruta '%s': %s", tipo, error)
            cls._sprites[tipo] = None

    @staticmethod
    def _ancho():
        return TAMANIO_FRUTA

    @staticmethod
    def _alto():
        return TAMANIO_FRUTA

    def recolectar(self):
        """Marca la fruta como recolectada y devuelve sus puntos."""
        self.activa = False
        return self.puntos

    def get_sprite(self):
        """Devuelve el sprite del tipo de fruta."""
        return self._sprites.get(self.tipo)

    def get_float_offset(self):
        """Desplazamiento vertical suave para el efecto de flotación."""
        t = (pygame.time.get_ticks() - self.start_time) / 1000.0
        return int(
            3 * pygame.math.Vector2(1, 0).rotate(t * 240 + self.float_offset).y
        )
