import pygame
import random
from src.constants import TILE_SIZE, COLOR_PARED, COLOR_BORDE_PARED, COLOR_CAMINO, COLOR_BORDE_CAMINO
from src.world.seeds import SEMILLAS


class Maze:
    def __init__(self, nivel):
        self.nivel = nivel
        self.tile_size = TILE_SIZE
        semilla_idx = random.randint(0, len(SEMILLAS[nivel]) - 1)
        self.mapa = SEMILLAS[nivel][semilla_idx]
        self.ancho = len(self.mapa[0]) * self.tile_size
        self.alto = len(self.mapa) * self.tile_size

    def obtener_posiciones_libres(self):
        posiciones = []
        for y, fila in enumerate(self.mapa):
            for x, celda in enumerate(fila):
                if celda == "0":
                    px = x * self.tile_size + self.tile_size // 2
                    py = y * self.tile_size + self.tile_size // 2
                    posiciones.append((px, py))
        return posiciones

    def colisiona(self, rect):
        tile_size = self.tile_size
        izquierda = max(0, rect.left // tile_size)
        derecha = min(len(self.mapa[0]) - 1, rect.right // tile_size)
        arriba = max(0, rect.top // tile_size)
        abajo = min(len(self.mapa) - 1, rect.bottom // tile_size)

        for y in range(arriba, abajo + 1):
            for x in range(izquierda, derecha + 1):
                if self.mapa[y][x] == "1":
                    tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    if rect.colliderect(tile_rect):
                        return True
        return False

    def dibujar(self, pantalla, camera):
        for y, fila in enumerate(self.mapa):
            for x, celda in enumerate(fila):
                rect = pygame.Rect(
                    x * self.tile_size - camera.x,
                    y * self.tile_size - camera.y,
                    self.tile_size,
                    self.tile_size,
                )
                if celda == "1":
                    pygame.draw.rect(pantalla, COLOR_PARED, rect)
                    pygame.draw.rect(pantalla, COLOR_BORDE_PARED, rect, 1)
                else:
                    pygame.draw.rect(pantalla, COLOR_CAMINO, rect)
                    pygame.draw.rect(pantalla, COLOR_BORDE_CAMINO, rect, 1)
