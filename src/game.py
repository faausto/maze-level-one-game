import pygame
import sys
import random
from src.ui import fonts
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
    NIVELES,
    SEMILLAS,
    FRUTAS_POR_NIVEL,
    MONSTRUOS_POR_NIVEL,
    SALIDAS,
)
from src.db.database import Database
from src.screens.menu import MenuScreen
from src.screens.instructions import InstructionsScreen
from src.screens.game_screen import GameScreen
from src.screens.result import ResultScreen
from src.screens.name_input import NameInputScreen
from src.screens.ranking import RankingScreen
from src.screens.final import FinalScreen


class EstadoJuego:
    MENU = "menu"
    INSTRUCCIONES = "instrucciones"
    JUEGO = "juego"
    RESULTADO = "resultado"
    RANKING = "ranking"
    FINAL = "final"
    INGRESO_NOMBRE = "ingreso_nombre"


class Juego:
    def __init__(self):
        pygame.init()
        fonts.inicializar_fuentes()
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Maze Level One Game")
        self.clock = pygame.time.Clock()

        self.estado_juego = EstadoJuego
        self.estado = EstadoJuego.MENU
        self.opcion_menu = 0
        self.opciones_menu = ["Jugar", "Instrucciones", "Tabla de puntos", "Salir"]
        self.texto_nombre = ""
        self.mensaje_resultado = ""
        self.puntaje_final = 0
        self.nivel_actual = 0
        self.vidas = 5
        self.puntaje = 0
        self.objetivo = pygame.Rect(0, 0, 40, 40)
        self.database = Database()

        self.menu_screen = MenuScreen()
        self.instructions_screen = InstructionsScreen()
        self.game_screen = GameScreen()
        self.result_screen = ResultScreen()
        self.name_input_screen = NameInputScreen()
        self.ranking_screen = RankingScreen()
        self.final_screen = FinalScreen()

        self.reiniciar_partida()

    def reiniciar_partida(self):
        self.nivel_actual = 0
        self.vidas = 5
        self.puntaje = 0
        self.objetivo = pygame.Rect(0, 0, 40, 40)
        self.cargar_nivel(0)

    def cargar_nivel(self, nivel):
        self.nivel_actual = nivel
        self.game_screen.cargar_nivel(nivel, self)

    def cargar_ranking(self):
        self.database.cargar_ranking()

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.estado == EstadoJuego.MENU:
                self.menu_screen.handle_event(self, event)
            elif self.estado == EstadoJuego.INSTRUCCIONES:
                self.instructions_screen.handle_event(self, event)
            elif self.estado == EstadoJuego.JUEGO:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.estado = EstadoJuego.MENU
            elif self.estado == EstadoJuego.RESULTADO:
                self.result_screen.handle_event(self, event)
            elif self.estado == EstadoJuego.INGRESO_NOMBRE:
                self.name_input_screen.handle_event(self, event)
            elif self.estado == EstadoJuego.RANKING:
                self.ranking_screen.handle_event(self, event)
            elif self.estado == EstadoJuego.FINAL:
                self.final_screen.handle_event(self, event)

    def actualizar(self, dt):
        if self.estado == EstadoJuego.JUEGO:
            self.game_screen.update(self, dt)

    def dibujar(self):
        if self.estado == EstadoJuego.MENU:
            self.menu_screen.draw(self)
        elif self.estado == EstadoJuego.INSTRUCCIONES:
            self.instructions_screen.draw(self)
        elif self.estado == EstadoJuego.JUEGO:
            self.game_screen.draw(self)
        elif self.estado == EstadoJuego.RESULTADO:
            self.result_screen.draw(self)
        elif self.estado == EstadoJuego.INGRESO_NOMBRE:
            self.name_input_screen.draw(self)
        elif self.estado == EstadoJuego.RANKING:
            self.ranking_screen.draw(self)
        elif self.estado == EstadoJuego.FINAL:
            self.final_screen.draw(self)

    def ejecutar(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
            self.manejar_eventos()
            self.actualizar(dt)
            self.dibujar()


if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()
