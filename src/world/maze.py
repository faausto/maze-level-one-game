"""Laberinto: mapa, colisiones y dibujo de las celdas visibles."""

import logging
import random

import pygame

from src.constants import (
    COLOR_BORDE_CAMINO,
    COLOR_BORDE_PARED,
    COLOR_CAMINO,
    COLOR_PARED,
    HUD_HEIGHT,
    IMAGES_DIR,
    TILE_SIZE,
)
from src.world.seeds import SEMILLAS

logger = logging.getLogger(__name__)


class Maze:
    """Representa un laberinto y resuelve sus colisiones y dibujo."""

    _grass_tile = None
    _rock_tile = None

    def __init__(self, nivel):
        self.nivel = nivel
        self.tile_size = TILE_SIZE
        semilla_idx = random.randint(0, len(SEMILLAS[nivel]) - 1)
        self.mapa = list(SEMILLAS[nivel][semilla_idx])
        self.ancho = len(self.mapa[0]) * self.tile_size
        self.alto = len(self.mapa) * self.tile_size
        self.spawn = self._buscar_celda("S")
        self.salida = self._buscar_celda("E")

        if Maze._grass_tile is None or Maze._rock_tile is None:
            self._cargar_texturas()

    def _buscar_celda(self, caracter):
        """Devuelve el rectángulo de la primera celda con el caracter dado."""
        for y, fila in enumerate(self.mapa):
            x = fila.find(caracter)
            if x != -1:
                return pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
        raise ValueError(f"La semilla no tiene la celda '{caracter}'")

    def _cargar_texturas(self):
        try:
            grass_img = pygame.image.load(
                IMAGES_DIR / "background" / "grass_background.png"
            ).convert()
            rock_img = pygame.image.load(
                IMAGES_DIR / "background" / "rock_background.png"
            ).convert_alpha()

            Maze._grass_tile = pygame.transform.scale(
                grass_img, (self.tile_size, self.tile_size)
            )
            Maze._rock_tile = pygame.transform.scale(
                rock_img, (self.tile_size, self.tile_size)
            )
        except (pygame.error, OSError) as error:
            logger.warning("No se pudieron cargar las texturas del laberinto: %s", error)
            Maze._grass_tile = None
            Maze._rock_tile = None

    def obtener_posiciones_libres(self):
        """Devuelve el centro de cada celda transitable del mapa."""
        posiciones = []
        for y, fila in enumerate(self.mapa):
            for x, celda in enumerate(fila):
                if celda == "0":
                    px = x * self.tile_size + self.tile_size // 2
                    py = y * self.tile_size + self.tile_size // 2
                    posiciones.append((px, py))
        return posiciones

    def colisiona(self, rect):
        """Indica si el rectángulo se superpone con alguna pared."""
        tile_size = self.tile_size
        izquierda = max(0, rect.left // tile_size)
        derecha = min(len(self.mapa[0]) - 1, rect.right // tile_size)
        arriba = max(0, rect.top // tile_size)
        abajo = min(len(self.mapa) - 1, rect.bottom // tile_size)

        for y in range(arriba, abajo + 1):
            for x in range(izquierda, derecha + 1):
                celda = self.mapa[y][x]
                if celda == "1":
                    tile_rect = pygame.Rect(
                        x * tile_size, y * tile_size, tile_size, tile_size
                    )
                    if rect.colliderect(tile_rect):
                        return True
        return False

    def dibujar(self, pantalla, camera, offset_y=HUD_HEIGHT):
        """Dibuja únicamente las celdas que entran en la pantalla."""
        tile_size = self.tile_size
        col_ini, col_fin, fila_ini, fila_fin = self._rango_visible(camera)

        for y in range(fila_ini, fila_fin):
            fila = self.mapa[y]
            for x in range(col_ini, col_fin):
                rect = pygame.Rect(
                    x * tile_size - camera.x,
                    y * tile_size - camera.y + offset_y,
                    tile_size,
                    tile_size,
                )
                self._dibujar_celda(pantalla, fila[x], rect)

    def _rango_visible(self, camera):
        """Devuelve el rango de columnas y filas visibles en pantalla."""
        tile_size = self.tile_size
        col_ini = max(0, camera.x // tile_size)
        col_fin = min(
            len(self.mapa[0]), (camera.x + camera.ancho_pantalla) // tile_size + 1
        )
        fila_ini = max(0, camera.y // tile_size)
        fila_fin = min(
            len(self.mapa), (camera.y + camera.alto_pantalla) // tile_size + 1
        )
        return col_ini, col_fin, fila_ini, fila_fin

    def _dibujar_celda(self, pantalla, celda, rect):
        """Dibuja una celda usando su textura o un color de respaldo."""
        if celda == "1":
            if Maze._rock_tile:
                pantalla.blit(Maze._rock_tile, rect)
            else:
                pygame.draw.rect(pantalla, COLOR_PARED, rect)
                pygame.draw.rect(pantalla, COLOR_BORDE_PARED, rect, 1)
        elif celda == "2":
            if Maze._rock_tile:
                pantalla.blit(Maze._rock_tile, rect)
                pygame.draw.rect(pantalla, (40, 255, 150), rect, 2)
            else:
                pygame.draw.rect(pantalla, COLOR_PARED, rect)
                pygame.draw.rect(pantalla, COLOR_BORDE_PARED, rect, 1)
        else:
            if Maze._grass_tile:
                pantalla.blit(Maze._grass_tile, rect)
            else:
                pygame.draw.rect(pantalla, COLOR_CAMINO, rect)
                pygame.draw.rect(pantalla, COLOR_BORDE_CAMINO, rect, 1)
