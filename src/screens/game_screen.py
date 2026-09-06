import pygame
from src.world.maze import Maze

ANCHO_PANTALLA = 800
TILE_SIZE = 60
VELOCIDAD_JUGADOR = 300

COLOR_FONDO = (75, 90, 60)
COLOR_PARED = (60, 60, 80)
COLOR_BORDE_PARED = (90, 105, 70)
COLOR_CAMINO = (75, 90, 60)
COLOR_BORDE_CAMINO = (65, 78, 50)
COLOR_OBJETIVO = (255, 80, 80)
COLOR_JUGADOR = (0, 120, 255)


class GameScreen:
    def __init__(self):
        self.maze = None
        self.camera_x = 0
        self.camera_y = 0
        self.player_rect = None
        self.objetivo = None

    def cargar_nivel(self, juego):
        self.maze = Maze(0)
        self.camera_x = 0
        self.camera_y = 0
        posiciones = self.maze.obtener_posiciones_libres()

        spawn = posiciones[0] if posiciones else (50, 50)
        self.player_rect = pygame.Rect(spawn[0] - 20, spawn[1] - 20, 40, 40)

        objetivo_pos = posiciones[1] if len(posiciones) > 1 else (spawn[0] + 100, spawn[1])
        juego.objetivo = pygame.Rect(objetivo_pos[0] - 20, objetivo_pos[1] - 20, 40, 40)

    def update(self, juego, dt):
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

        nuevo_rect = self.player_rect.move(dx, 0)
        if not self.maze.colisiona(nuevo_rect):
            self.player_rect.x = nuevo_rect.x
        nuevo_rect = self.player_rect.move(0, dy)
        if not self.maze.colisiona(nuevo_rect):
            self.player_rect.y = nuevo_rect.y
        self.player_rect.clamp_ip(pygame.Rect(0, 0, self.maze.ancho, self.maze.alto))

        self.camera_x = self.player_rect.centerx - ANCHO_PANTALLA // 2
        self.camera_y = self.player_rect.centery - 600 // 2
        self.camera_x = max(0, min(self.camera_x, self.maze.ancho - ANCHO_PANTALLA))
        self.camera_y = max(0, min(self.camera_y, self.maze.alto - 600))

    def draw(self, juego):
        pantalla = juego.pantalla
        pantalla.fill(COLOR_FONDO)

        self.maze.dibujar(pantalla, self.camera_x, self.camera_y)

        objetivo_pantalla = pygame.Rect(
            juego.objetivo.x - self.camera_x,
            juego.objetivo.y - self.camera_y,
            juego.objetivo.width,
            juego.objetivo.height,
        )
        pygame.draw.rect(pantalla, COLOR_OBJETIVO, objetivo_pantalla)

        jugador_pantalla = pygame.Rect(
            self.player_rect.x - self.camera_x,
            self.player_rect.y - self.camera_y,
            self.player_rect.width,
            self.player_rect.height,
        )
        pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador_pantalla)

        pygame.display.flip()
