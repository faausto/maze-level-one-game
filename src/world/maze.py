import pygame
from src.constants import TILE_SIZE, COLOR_PARED, COLOR_BORDE_PARED, COLOR_CAMINO, COLOR_BORDE_CAMINO


class Maze:
    def __init__(self, nivel):
        self.nivel = nivel
        self.tile_size = TILE_SIZE
        self.mapa = [
            "11111111111111111111",
            "10000000000000000001",
            "10111101111101111101",
            "10100000000000001001",
            "10101111111111101001",
            "10000000000000000001",
            "11110111101111101111",
            "10000100000010000001",
            "10111011101110111101",
            "10000000000000000001",
            "10111101111101111101",
            "10000000000000000001",
            "11111111111111111111",
        ]
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
