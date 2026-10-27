import pygame
import os
from src.entities.animation import DirectionalAnimation


class Player:
    def __init__(self, x, y, ancho=40, alto=40):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.velocidad = 300
        self.ancho = ancho
        self.alto = alto
        self.visual_scale = 1.5
        self.visual_ancho = int(ancho * self.visual_scale)
        self.visual_alto = int(alto * self.visual_scale)

        base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'images', 'player')

        self.walk_animation = DirectionalAnimation(
            os.path.join(base_path, 'walk'), 'walk', 126, 132, 4, 3, fps=12, loop=True
        )
        self.idle_animation = DirectionalAnimation(
            os.path.join(base_path, 'idle'), 'idle', 126, 132, 6, 6, fps=8, loop=True, total_frames=31
        )

        self.current_animation = self.idle_animation
        self.last_dx = 0
        self.last_dy = 0
        self.is_moving = False

    def mover(self, dx, dy, maze, mundo_rect):
        nuevo_rect = self.rect.move(dx, 0)
        if not maze.colisiona(nuevo_rect):
            self.rect.x = nuevo_rect.x
        nuevo_rect = self.rect.move(0, dy)
        if not maze.colisiona(nuevo_rect):
            self.rect.y = nuevo_rect.y
        self.rect.clamp_ip(mundo_rect)

        was_moving = self.is_moving
        self.is_moving = dx != 0 or dy != 0

        if self.is_moving:
            self.last_dx = dx
            self.last_dy = dy
            direction = self.walk_animation.get_direction_from_vector(dx, dy)
            self.walk_animation.set_direction(direction)
            self.idle_animation.set_direction(direction)
            if self.current_animation != self.walk_animation:
                self.current_animation = self.walk_animation
                self.walk_animation.reset()
        else:
            if self.current_animation != self.idle_animation:
                self.current_animation = self.idle_animation
                self.idle_animation.reset()

    def update(self, dt):
        self.current_animation.update(dt)

    def get_current_sprite(self):
        frame = self.current_animation.get_current_frame()
        if frame:
            return pygame.transform.scale(frame, (self.visual_ancho, self.visual_alto))
        return None

    def get_draw_offset(self):
        offset_x = (self.visual_ancho - self.ancho) // 2
        offset_y = (self.visual_alto - self.alto) // 2
        return offset_x, offset_y

    def get_rect(self):
        return self.rect