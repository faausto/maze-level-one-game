import pygame
import sys
from src.screens.game_screen import GameScreen


ANCHO_PANTALLA, ALTO_PANTALLA = 800, 600
COLOR_FONDO = (75, 90, 60)


class EstadoJuego:
    JUEGO = "juego"


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Maze Level One Game")
        self.clock = pygame.time.Clock()

        self.estado = EstadoJuego.JUEGO
        self.estado_juego = EstadoJuego
        self.game_screen = GameScreen()
        self.game_screen.cargar_nivel(self)

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def actualizar(self, dt):
        if self.estado == EstadoJuego.JUEGO:
            self.game_screen.update(self, dt)

    def dibujar(self):
        if self.estado == EstadoJuego.JUEGO:
            self.game_screen.draw(self)

    def ejecutar(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
            self.manejar_eventos()
            self.actualizar(dt)
            self.dibujar()


if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()
