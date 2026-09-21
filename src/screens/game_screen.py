import pygame
import random
from src.constants import (
    COLOR_FONDO,
    COLOR_PARED,
    COLOR_BORDE_PARED,
    COLOR_CAMINO,
    COLOR_BORDE_CAMINO,
    COLOR_OBJETIVO,
    COLOR_JUGADOR,
    COLOR_TITULO,
    ANCHO_PANTALLA,
    TILE_SIZE,
    VELOCIDAD_JUGADOR,
    SEMILLAS,
)
from src.world.maze import Maze
from src.world.camera import Camera
from src.entities.player import Player


class GameScreen:
    def __init__(self):
        self.maze = None
        self.camera = None
        self.player = None
        self.objetivo = None

    def cargar_nivel(self, nivel, juego):
        self.maze = Maze(nivel)
        self.camera = Camera(self.maze.ancho, self.maze.alto, ANCHO_PANTALLA, 600)
        mundo_rect = pygame.Rect(0, 0, self.maze.ancho, self.maze.alto)
        posiciones = self.maze.obtener_posiciones_libres()

        spawn = posiciones[0] if posiciones else (50, 50)
        self.player = Player(spawn[0] - 20, spawn[1] - 20)

        objetivo_pos = posiciones[1] if len(posiciones) > 1 else (spawn[0] + 100, spawn[1])
        juego.objetivo = pygame.Rect(objetivo_pos[0] - 20, objetivo_pos[1] - 20, 40, 40)

    def update(self, juego, dt):
        if juego.estado != juego.estado_juego.JUEGO:
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -VELOCIDAD_JUGADOR * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = VELOCIDAD_JUGADOR * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -VELOCIDAD_JUGADOR * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = VELOCIDAD_JUGADOR * dt

        mundo_rect = pygame.Rect(0, 0, self.maze.ancho, self.maze.alto)
        self.player.mover(dx, dy, self.maze, mundo_rect)

    def draw(self, juego):
        self.camera.update(self.player.get_rect())
        pantalla = juego.pantalla
        pantalla.fill(COLOR_FONDO)

        self.maze.dibujar(pantalla, self.camera)

        objetivo_pantalla = self.camera.aplicar(juego.objetivo)
        pygame.draw.rect(pantalla, COLOR_OBJETIVO, objetivo_pantalla)

        jugador_pantalla = self.camera.aplicar(self.player.get_rect())
        pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador_pantalla)

        pygame.display.flip()
