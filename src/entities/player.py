"""Entidad del jugador: movimiento y animación en ocho direcciones."""

import pygame

from src.constants import IMAGES_DIR
from src.entities.animation import DirectionalAnimation


class Player:
    """Personaje controlado por el jugador."""

    def __init__(self, x, y, ancho=51, alto=51):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.ancho = ancho
        self.alto = alto
        self.visual_scale = 1.5
        self.visual_ancho = int(ancho * self.visual_scale)
        self.visual_alto = int(alto * self.visual_scale)

        base_path = IMAGES_DIR / "player"
        tamano = (self.visual_ancho, self.visual_alto)

        self.walk_animation = DirectionalAnimation(
            base_path / "walk",
            "walk",
            126,
            132,
            4,
            3,
            fps=12,
            loop=True,
            size=tamano,
        )
        self.idle_animation = DirectionalAnimation(
            base_path / "idle",
            "idle",
            126,
            132,
            6,
            6,
            fps=8,
            loop=True,
            total_frames=31,
            size=tamano,
        )

        self.current_animation = self.idle_animation
        self.is_moving = False

    def mover(self, dx, dy, maze, mundo_rect):
        """Mueve al jugador resolviendo las colisiones por eje."""
        nuevo_rect = self.rect.move(dx, 0)
        if not maze.colisiona(nuevo_rect):
            self.rect.x = nuevo_rect.x
        nuevo_rect = self.rect.move(0, dy)
        if not maze.colisiona(nuevo_rect):
            self.rect.y = nuevo_rect.y
        self.rect.clamp_ip(mundo_rect)

        self.is_moving = dx != 0 or dy != 0

        if self.is_moving:
            direction = self.walk_animation.get_direction_from_vector(dx, dy)
            self.walk_animation.set_direction(direction)
            self.idle_animation.set_direction(direction)
            if self.current_animation != self.walk_animation:
                self.current_animation = self.walk_animation
                self.walk_animation.reset()
        elif self.current_animation != self.idle_animation:
            self.current_animation = self.idle_animation
            self.idle_animation.reset()

    def update(self, dt):
        """Avanza la animación actual."""
        self.current_animation.update(dt)

    def get_current_sprite(self):
        """Devuelve el frame actual ya escalado al tamaño visual."""
        return self.current_animation.get_current_frame()

    def get_draw_offset(self):
        """Desplazamiento para centrar el sprite sobre el rectángulo de colisión."""
        offset_x = (self.visual_ancho - self.ancho) // 2
        offset_y = (self.visual_alto - self.alto) // 2
        return offset_x, offset_y
