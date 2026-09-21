import pygame
import sys
import random
from src.constants import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    COLOR_FONDO,
    COLOR_PARED,
    COLOR_BORDE,
    COLOR_JUGADOR,
    COLOR_OBJETIVO,
    COLOR_TEXTO,
    COLOR_TITULO,
)
from src.screens.menu import MenuScreen
from src.screens.game_screen import GameScreen


class EstadoJuego:
    MENU = "menu"
    JUEGO = "juego"


class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Maze Level One Game")
        self.clock = pygame.time.Clock()

        self.estado_juego = EstadoJuego
        self.estado = EstadoJuego.MENU
        self.opcion_menu = 0
        self.opciones_menu = ["Jugar", "Salir"]
        self.objetivo = pygame.Rect(0, 0, 40, 40)

        self.menu_screen = MenuScreen()
        self.game_screen = GameScreen()

        self.reiniciar_partida()

    def reiniciar_partida(self):
        self.objetivo = pygame.Rect(0, 0, 40, 40)
        self.cargar_nivel()

    def cargar_nivel(self):
        self.game_screen.cargar_nivel(self)

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.estado == EstadoJuego.MENU:
                self.menu_screen.handle_event(self, event)
            elif self.estado == EstadoJuego.JUEGO:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.estado = EstadoJuego.MENU

    def actualizar(self, dt):
        if self.estado == EstadoJuego.JUEGO:
            self.game_screen.update(self, dt)

    def dibujar(self):
        if self.estado == EstadoJuego.MENU:
            self.menu_screen.draw(self)
        elif self.estado == EstadoJuego.JUEGO:
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
