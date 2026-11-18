"""Entidad de los monstruos: patrulla, persecución y animación."""

import logging
import math
from collections import deque
from typing import ClassVar

import pygame

from src.constants import (
    IMAGES_DIR,
    INTERVALO_RECALCULO_CAMINO,
    PAUSA_MONSTRUO_TRAS_DANO,
)

logger = logging.getLogger(__name__)


class Monster:
    """Enemigo que patrulla el laberinto y puede perseguir al jugador."""

    _sprite_sheet = None
    _animations: ClassVar[dict] = {}
    _frame_size = 128
    _cols = 6
    _rows = 4

    def __init__(self, x, y, ancho, alto, patrulla, velocidad, rango_deteccion=0):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self._pos_x = float(x)
        self._pos_y = float(y)
        self.patrulla = patrulla
        self.indice_punto = 0
        self.camino_patrulla = None
        self.destino_patrulla = None
        self.velocidad = velocidad
        self.rango_deteccion = rango_deteccion
        self.persiguiendo = False
        self.camino = None
        self.tiempo_recalculo = 0.0
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
        else:
            self.persiguiendo = False

    def pausar_tras_dano(self):
        """Detiene al monstruo tras tocar al jugador antes de volver a patrullar."""
        self.tiempo_espera = PAUSA_MONSTRUO_TRAS_DANO
        self.persiguiendo = False
        self.camino = None
        self.camino_patrulla = None
        self.destino_patrulla = None

    def _desplazamiento(self, dx, dy, dt):
        vector = pygame.math.Vector2(dx, dy)
        if vector.length_squared() == 0:
            return 0.0, 0.0
        vector = vector.normalize() * self.velocidad * dt
        return vector.x, vector.y

    def _centro_celda(self, celda, maze):
        """Devuelve el centro en píxeles de una celda del laberinto."""
        x, y = celda
        tile = maze.tile_size
        return x * tile + tile // 2, y * tile + tile // 2

    def _bfs(self, maze, inicio, destino):
        """Busca un camino de celdas libres entre dos celdas."""
        if inicio == destino:
            return [inicio]

        cola = deque([inicio])
        previos = {inicio: None}
        while cola:
            actual = cola.popleft()
            if actual == destino:
                break
            x, y = actual
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if not (0 <= ny < len(maze.mapa) and 0 <= nx < len(maze.mapa[0])):
                    continue
                if maze.mapa[ny][nx] == "1" or (nx, ny) in previos:
                    continue
                previos[(nx, ny)] = actual
                cola.append((nx, ny))

        if destino not in previos:
            return []

        camino = []
        actual = destino
        while actual != inicio:
            camino.append(actual)
            actual = previos[actual]
        camino.reverse()
        return camino

    def _calcular_camino(self, maze, jugador_rect):
        """Busca con BFS un camino de celdas libres hasta el jugador."""
        tile = maze.tile_size
        inicio = (self.rect.centerx // tile, self.rect.centery // tile)
        destino = (
            jugador_rect.centerx // tile,
            jugador_rect.centery // tile,
        )
        return self._bfs(maze, inicio, destino)

    def _calcular_camino_celda(self, maze, destino):
        """Busca con BFS un camino de celdas libres hasta una celda."""
        tile = maze.tile_size
        inicio = (self.rect.centerx // tile, self.rect.centery // tile)
        return self._bfs(maze, inicio, destino)

    def _mover_hacia(self, dt, objetivo_x, objetivo_y, maze, mundo_rect):
        """Mueve el monstruo hacia un punto y devuelve (se movió, llegó)."""
        dx = objetivo_x - self.rect.centerx
        dy = objetivo_y - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia <= self.velocidad * dt:
            self.rect.center = (round(objetivo_x), round(objetivo_y))
            if mundo_rect:
                self.rect.clamp_ip(mundo_rect)
            self._pos_x = float(self.rect.x)
            self._pos_y = float(self.rect.y)
            return True, True
        if distancia <= 0:
            return False, True

        mov_x, mov_y = self._desplazamiento(dx, dy, dt)
        self._actualizar_direccion(mov_x, mov_y)

        # Ejes por separado y posición flotante: si un muro bloquea un eje,
        # el otro desliza sin perder las fracciones de píxel.
        nuevo_x = self.rect.copy()
        nuevo_x.x = round(self._pos_x + mov_x)
        if not maze.colisiona(nuevo_x):
            self._pos_x += mov_x

        nuevo_y = self.rect.copy()
        nuevo_y.x = round(self._pos_x)
        nuevo_y.y = round(self._pos_y + mov_y)
        if not maze.colisiona(nuevo_y):
            self._pos_y += mov_y

        self.rect.x = round(self._pos_x)
        self.rect.y = round(self._pos_y)
        if mundo_rect:
            self.rect.clamp_ip(mundo_rect)
            self._pos_x = float(self.rect.x)
            self._pos_y = float(self.rect.y)
        return True, False

    def _perseguir(self, dt, jugador_rect, maze, mundo_rect):
        """Sigue el camino BFS hacia el jugador sin atravesar paredes."""
        if self.camino is None:
            self._pos_x = float(self.rect.x)
            self._pos_y = float(self.rect.y)
        if self.camino is None or not self.camino or self.tiempo_recalculo <= 0:
            self.camino = self._calcular_camino(maze, jugador_rect)
            self.tiempo_recalculo = INTERVALO_RECALCULO_CAMINO
        self.tiempo_recalculo -= dt

        if not self.camino:
            self.persiguiendo = False
            self.tiempo_espera = 0.2
            return False

        tile = maze.tile_size
        celda_actual = (self.rect.centerx // tile, self.rect.centery // tile)
        if len(self.camino) == 1 and self.camino[0] == celda_actual:
            objetivo_x = jugador_rect.centerx
            objetivo_y = jugador_rect.centery
        else:
            objetivo_x, objetivo_y = self._centro_celda(self.camino[0], maze)

        movido, llego = self._mover_hacia(
            dt, objetivo_x, objetivo_y, maze, mundo_rect
        )
        if llego and len(self.camino) > 1:
            self.camino.pop(0)
        return movido

    def _siguiente_punto_patrulla(self):
        """Avanza al siguiente punto del circuito de patrulla."""
        self.indice_punto = (self.indice_punto + 1) % len(self.patrulla)
        self.camino_patrulla = None
        self.destino_patrulla = None

    def _iniciar_camino_patrulla(self, maze, destino):
        """Calcula el camino hacia el punto de patrulla actual."""
        self.camino_patrulla = self._calcular_camino_celda(maze, destino)
        self.destino_patrulla = destino
        self._pos_x = float(self.rect.x)
        self._pos_y = float(self.rect.y)

    def _patrullar(self, dt, maze, mundo_rect):
        """Recorre el circuito de puntos libres asignado al monstruo."""
        if not (self.patrulla and maze):
            return False

        destino = self.patrulla[self.indice_punto]
        if self.camino_patrulla is None or self.destino_patrulla != destino:
            self._iniciar_camino_patrulla(maze, destino)

        if not self.camino_patrulla:
            self._siguiente_punto_patrulla()
            return False

        tile = maze.tile_size
        celda_actual = (self.rect.centerx // tile, self.rect.centery // tile)
        if len(self.camino_patrulla) == 1 and self.camino_patrulla[0] == celda_actual:
            centro_x, centro_y = self._centro_celda(destino, maze)
            distancia = math.hypot(
                centro_x - self.rect.centerx,
                centro_y - self.rect.centery,
            )
            if distancia < 2:
                self._siguiente_punto_patrulla()
                return False

        objetivo_x, objetivo_y = self._centro_celda(
            self.camino_patrulla[0], maze
        )
        movido, llego = self._mover_hacia(
            dt, objetivo_x, objetivo_y, maze, mundo_rect
        )
        if llego:
            if len(self.camino_patrulla) > 1:
                self.camino_patrulla.pop(0)
            else:
                self.camino_patrulla = None
                self._siguiente_punto_patrulla()
        return movido

    def update(self, dt, jugador_rect, maze=None, mundo_rect=None):
        """Actualiza animación, patrulla o persecución del monstruo."""
        self._avanzar_animacion(dt)

        if self.tiempo_espera > 0:
            self.tiempo_espera -= dt
            return

        self._actualizar_persecucion(jugador_rect, maze)

        if self.persiguiendo and jugador_rect and maze:
            self.camino_patrulla = None
            self.destino_patrulla = None
            self.is_moving = self._perseguir(dt, jugador_rect, maze, mundo_rect)
        else:
            self.camino = None
            self.is_moving = self._patrullar(dt, maze, mundo_rect)
