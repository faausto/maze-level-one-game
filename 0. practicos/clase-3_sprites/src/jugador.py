import pygame


class Jugador(pygame.sprite.Sprite):
    def __init__(self, pantalla_rect):
        super().__init__()
        self.image = pygame.image.load("assets/images/nave.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(400, 300))
        self.velocidad = 300
        self.pantalla_rect = pantalla_rect
        self.timer_disparo = 0.0
        self.cadencia = 0.2

    def update(self, dt, teclas, disparos):
        dx = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * self.velocidad * dt
        dy = (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * self.velocidad * dt
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(self.pantalla_rect)

        self.timer_disparo += dt
        if teclas[pygame.K_SPACE] and self.timer_disparo >= self.cadencia:
            self.timer_disparo = 0.0
            disparo = Disparo(self.rect.centerx, self.rect.top)
            disparos.add(disparo)


class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.velocidad = -500

    def update(self, dt):
        self.rect.y += self.velocidad * dt
        if self.rect.bottom < 0:
            self.kill()