import pygame
import random
import os
from src.constants import TILE_SIZE, COLOR_PARED, COLOR_BORDE_PARED, COLOR_CAMINO, COLOR_BORDE_CAMINO
from src.world.seeds import SEMILLAS


class Maze:
    _grass_tile = None
    _rock_tile = None

    def __init__(self, nivel):
        self.nivel = nivel
        self.tile_size = TILE_SIZE
        semilla_idx = random.randint(0, len(SEMILLAS[nivel]) - 1)
        self.mapa = SEMILLAS[nivel][semilla_idx]
        self.ancho = len(self.mapa[0]) * self.tile_size
        self.alto = len(self.mapa) * self.tile_size

        if Maze._grass_tile is None or Maze._rock_tile is None:
            self._cargar_texturas()

    def _cargar_texturas(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            grass_path = os.path.join(base_dir, "assets", "images", "background", "grass_background.png")
            rock_path = os.path.join(base_dir, "assets", "images", "background", "rock_background.png")

            grass_img = pygame.image.load(grass_path).convert()
            rock_img = pygame.image.load(rock_path).convert_alpha()

            Maze._grass_tile = pygame.transform.scale(grass_img, (self.tile_size, self.tile_size))
            Maze._rock_tile = pygame.transform.scale(rock_img, (self.tile_size, self.tile_size))
        except Exception as e:
            print(f"Error cargando texturas de fondo: {e}")
            Maze._grass_tile = None
            Maze._rock_tile = None

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
                celda = self.mapa[y][x]
                if celda == "1":
                    tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    if rect.colliderect(tile_rect):
                        return True
        return False

    def dibujar(self, pantalla, camera, offset_y=80):
        for y, fila in enumerate(self.mapa):
            for x, celda in enumerate(fila):
                rect = pygame.Rect(
                    x * self.tile_size - camera.x,
                    y * self.tile_size - camera.y + offset_y,
                    self.tile_size,
                    self.tile_size,
                )
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
