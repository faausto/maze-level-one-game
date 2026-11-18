"""Entidad de los monstruos: patrulla, persecución y animación."""

import logging
import math
import random
from typing import ClassVar

import pygame

from src.constants import IMAGES_DIR

logger = logging.getLogger(__name__)


class Monster:
    """Enemigo que se mueve por el laberinto y puede perseguir al jugador."""

    _sprite_sheet = None
    _animations: ClassVar[dict] = {}
    _frame_size = 128
    _cols = 6
    _rows = 4

    def __init__(self, x, y, ancho, alto, puntos, velocidad, rango_deteccion=0):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.puntos = puntos
        self.indice_punto = 0
        self.velocidad = velocidad
        self.rango_deteccion = rango_deteccion
        self.persiguiendo = False
        self.objetivo_wander = None
        self.origen_wander = (x, y)
        self.max_distancia = random.randint(102, 205)
        self.tiempo_espera = 0
        self.visual_scale = 3.0
        self.visual_ancho = int(ancho * self.visual_scale)
        self.visual_alto = int(alto * self.visual_scale)
        self.dir_actual = "abajo"
        self.frame_index = 0
        self.frame_time = 0.12
        self.frame_timer = 0.0
        self.is_moving = False
        self._sprites_escalados = {}

        if Monster._sprite_sheet is None:
            self._load_sprites()
        self._escalar_frames()

    @classmethod
    def _load_sprites(cls):
        try:
            ruta = IMAGES_DIR / "monsters" / "witch.png"
            cls._sprite_sheet = pygame.image.load(ruta).convert_alpha()
            cls._animations = {
                "abajo": [],
                "izquierda": [],
                "derecha": [],
                "arriba": [],
            }
            row_map = {0: "abajo", 1: "izquierda", 2: "derecha", 3: "arriba"}
            for row in range(cls._rows):
                dir_name = row_map.get(row, "abajo")
                for col in range(cls._cols):
                    x = col * cls._frame_size
                    y = row * cls._frame_size
                    frame = cls._sprite_sheet.subsurface(
                        pygame.Rect(x, y, cls._frame_size, cls._frame_size)
                    )
                    cls._animations[dir_name].append(frame)
        except (pygame.error, OSError) as error:
            logger.warning("No se pudieron cargar los sprites del monstruo: %s", error)
            cls._animations = {"abajo": [], "izquierda": [], "derecha": [], "arriba": []}

    def _escalar_frames(self):
        """Escala una sola vez los frames al tamaño visual del monstruo."""
        tamano = (self.visual_ancho, self.visual_alto)
        self._sprites_escalados = {
            direccion: [
                pygame.transform.scale(frame, tamano) for frame in frames
            ]
            for direccion, frames in Monster._animations.items()
        }

    def _actualizar_direccion(self, dx, dy):
        if dx == 0 and dy == 0:
            return
        if abs(dx) > abs(dy):
            self.dir_actual = "derecha" if dx > 0 else "izquierda"
        else:
            self.dir_actual = "abajo" if dy > 0 else "arriba"

    def get_current_sprite(self):
        """Devuelve el frame actual ya escalado."""
        frames = self._sprites_escalados.get(self.dir_actual, [])
        if frames:
            return frames[self.frame_index % len(frames)]
        return None

    def get_draw_offset(self):
        """Desplazamiento para centrar el sprite sobre el rectángulo de colisión."""
        offset_x = (self.visual_ancho - self.rect.width) // 2
        offset_y = (self.visual_alto - self.rect.height) // 2
        return offset_x, offset_y - 10

    def _es_celda_valida(self, maze, x, y):
        if not maze:
            return True
        tile_size = maze.tile_size
        cx = int(x // tile_size)
        cy = int(y // tile_size)
        if cy < 0 or cy >= len(maze.mapa) or cx < 0 or cx >= len(maze.mapa[0]):
            return False
        if maze.mapa[cy][cx] == "1":
            return False
        test_rect = pygame.Rect(int(x), int(y), self.rect.width, self.rect.height)
        return not maze.colisiona(test_rect)

    def _generar_objetivo_wander(self, maze):
        if not maze:
            return
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(direcciones)
        for dx_dir, dy_dir in direcciones:
            dist_candidata = random.randint(60, self.max_distancia)
            nx = self.rect.x + dx_dir * dist_candidata
            ny = self.rect.y + dy_dir * dist_candidata
            if self._es_celda_valida(maze, nx, ny):
                self.objetivo_wander = (nx, ny)
                self.origen_wander = (self.rect.x, self.rect.y)
                return
        self.objetivo_wander = (self.origen_wander[0], self.origen_wander[1])

    def _avanzar_animacion(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.frame_index += 1

    def _actualizar_persecucion(self, jugador_rect, maze):
        if self.rango_deteccion > 0 and jugador_rect and maze:
            dist_jugador = math.hypot(
                jugador_rect.centerx - self.rect.centerx,
                jugador_rect.centery - self.rect.centery,
            )
            self.persiguiendo = dist_jugador <= self.rango_deteccion

    def _desplazamiento(self, dx, dy, dt):
        vector = pygame.math.Vector2(dx, dy)
        if vector.length_squared() == 0:
            return 0.0, 0.0
        vector = vector.normalize() * self.velocidad * dt
        return vector.x, vector.y

    def _perseguir(self, dt, jugador_rect, maze, mundo_rect):
        objetivo_x = jugador_rect.centerx - self.rect.width // 2
        objetivo_y = jugador_rect.centery - self.rect.height // 2
        dx = objetivo_x - self.rect.x
        dy = objetivo_y - self.rect.y
        dist = math.hypot(dx, dy)
        movido = False

        if dist > 0:
            mov_x, mov_y = self._desplazamiento(dx, dy, dt)
            self._actualizar_direccion(mov_x, mov_y)

            nuevo_x = self.rect.move(mov_x, 0)
            if not maze.colisiona(nuevo_x):
                self.rect.x = nuevo_x.x
                movido = True
            else:
                self.persiguiendo = False
                self.tiempo_espera = 0.2

            nuevo_y = self.rect.move(0, mov_y)
            if not maze.colisiona(nuevo_y):
                self.rect.y = nuevo_y.y
                movido = True
            else:
                self.persiguiendo = False
                self.tiempo_espera = 0.2

            if mundo_rect:
                self.rect.clamp_ip(mundo_rect)

        return movido or dist > 0.1

    def _patrullar(self, dt, maze, mundo_rect):
        if not (self.puntos and maze):
            return False

        objetivo_x, objetivo_y = self.puntos[self.indice_punto]
        dx = objetivo_x - self.rect.x
        dy = objetivo_y - self.rect.y
        dist = math.hypot(dx, dy)

        if dist < max(2, self.velocidad * dt):
            self.rect.x = objetivo_x
            self.rect.y = objetivo_y
            self.indice_punto = (self.indice_punto + 1) % len(self.puntos)
            return False
        if dist <= 0:
            return False

        mov_x, mov_y = self._desplazamiento(dx, dy, dt)
        self._actualizar_direccion(mov_x, mov_y)

        nuevo_x = self.rect.move(mov_x, 0)
        if not maze.colisiona(nuevo_x):
            self.rect.x = nuevo_x.x
        nuevo_y = self.rect.move(0, mov_y)
        if not maze.colisiona(nuevo_y):
            self.rect.y = nuevo_y.y
        if mundo_rect:
            self.rect.clamp_ip(mundo_rect)
        return True

    def _vagar(self, dt, maze, mundo_rect):
        objetivo_x, objetivo_y = self.objetivo_wander
        dx = objetivo_x - self.rect.x
        dy = objetivo_y - self.rect.y
        dist = math.hypot(dx, dy)

        if dist < 4:
            self._alcanzar_objetivo_wander(maze)
            return False
        if dist <= 0:
            return False

        mov_x, mov_y = self._desplazamiento(dx, dy, dt)
        self._actualizar_direccion(mov_x, mov_y)

        if not self._aplicar_movimiento_vagar(mov_x, mov_y, maze):
            return False

        if mundo_rect:
            self.rect.clamp_ip(mundo_rect)
        return True

    def _alcanzar_objetivo_wander(self, maze):
        """Elige un destino nuevo o vuelve al origen del patrullaje."""
        if self.objetivo_wander == self.origen_wander:
            self._generar_objetivo_wander(maze)
            self.max_distancia = random.randint(102, 205)
        else:
            self.objetivo_wander = tuple(self.origen_wander)

    def _aplicar_movimiento_vagar(self, mov_x, mov_y, maze):
        """Mueve al monstruo; ante una pared vuelve al origen y se detiene."""
        if not maze:
            self.rect.x += mov_x
            self.rect.y += mov_y
            return True

        nuevo_x = self.rect.move(mov_x, 0)
        if maze.colisiona(nuevo_x):
            self.objetivo_wander = tuple(self.origen_wander)
            return False
        self.rect.x = nuevo_x.x

        nuevo_y = self.rect.move(0, mov_y)
        if maze.colisiona(nuevo_y):
            self.objetivo_wander = tuple(self.origen_wander)
            return False
        self.rect.y = nuevo_y.y
        return True

    def update(self, dt, jugador_rect, maze=None, mundo_rect=None):
        """Actualiza animación y movimiento del monstruo."""
        self._avanzar_animacion(dt)

        if self.tiempo_espera > 0:
            self.tiempo_espera -= dt
            return

        self._actualizar_persecucion(jugador_rect, maze)

        if self.persiguiendo and jugador_rect and maze:
            self.is_moving = self._perseguir(dt, jugador_rect, maze, mundo_rect)
        elif maze is None or self.objetivo_wander is None:
            self.is_moving = self._patrullar(dt, maze, mundo_rect)
        else:
            self.is_moving = self._vagar(dt, maze, mundo_rect)
