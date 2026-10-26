import pygame


class Monster:
    def __init__(self, x, y, ancho, alto, puntos, velocidad, rango_deteccion=0):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.puntos = puntos
        self.indice_punto = 0
        self.direccion = 1
        self.velocidad = velocidad
        self.rango_deteccion = rango_deteccion
        self.persiguiendo = False

    def update(self, dt, jugador_rect):
        if self.rango_deteccion > 0:
            dist = (
                (jugador_rect.centerx - self.rect.centerx) ** 2
                + (jugador_rect.centery - self.rect.centery) ** 2
            ) ** 0.5
            self.persiguiendo = dist <= self.rango_deteccion

        objetivo = self.puntos[self.indice_punto]
        dx_m = objetivo[0] - self.rect.x
        dy_m = objetivo[1] - self.rect.y
        dist_m = (dx_m ** 2 + dy_m ** 2) ** 0.5

        if dist_m < self.velocidad * dt:
            self.rect.x = objetivo[0]
            self.rect.y = objetivo[1]
            self.indice_punto = (self.indice_punto + self.direccion) % len(self.puntos)
        else:
            angulo = pygame.math.Vector2(dx_m, dy_m).normalize()
            self.rect.x += angulo.x * self.velocidad * dt
            self.rect.y += angulo.y * self.velocidad * dt

    def get_rect(self):
        return self.rect
