"""Bucle principal del juego y coordinación de las pantallas."""

import sys

import pygame

from src.audio import Audio
from src.constants import ALTO_PANTALLA, ANCHO_PANTALLA, FPS, VIDAS_INICIALES
from src.db.database import Database
from src.estados import EstadoJuego
from src.screens.final import FinalScreen
from src.screens.game_screen import GameScreen
from src.screens.instructions import InstructionsScreen
from src.screens.menu import MenuScreen
from src.screens.name_input import NameInputScreen
from src.screens.ranking import RankingScreen
from src.screens.result import ResultScreen
from src.ui import fonts


class Juego:
    """Coordina el estado, las pantallas y el bucle principal."""

    def __init__(self):
        self._inicializar_ventana()
        self._inicializar_estado()

        self.database = Database()
        self.audio = Audio()
        self.pantallas = self._crear_pantallas()

        self.reiniciar_partida()
        self._actualizar_audio()

    def _inicializar_ventana(self):
        """Inicializa pygame, la ventana y los recursos gráficos."""
        pygame.init()
        fonts.inicializar_fuentes()
        self.fullscreen = False
        self.display = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Maze Level One Game")
        self.pantalla = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        self.clock = pygame.time.Clock()

    def _inicializar_estado(self):
        """Deja el estado de la partida en sus valores iniciales."""
        self.estado = EstadoJuego.MENU
        self.opcion_menu = 0
        self.opciones_menu = [
            "Jugar",
            "Instrucciones",
            "Tabla de puntos",
            "Salir",
        ]
        self.texto_nombre = ""
        self.mensaje_nombre = ""
        self.mensaje_resultado = ""
        self.puntaje_final = 0
        self.nivel_actual = 0
        self.vidas = VIDAS_INICIALES
        self.puntaje = 0

    def _crear_pantallas(self):
        """Crea el mapa de estados a pantallas."""
        return {
            EstadoJuego.MENU: MenuScreen(),
            EstadoJuego.INSTRUCCIONES: InstructionsScreen(),
            EstadoJuego.JUEGO: GameScreen(),
            EstadoJuego.RESULTADO: ResultScreen(),
            EstadoJuego.INGRESO_NOMBRE: NameInputScreen(),
            EstadoJuego.RANKING: RankingScreen(),
            EstadoJuego.RANKING_VICTORIA: RankingScreen(),
            EstadoJuego.FINAL: FinalScreen(),
        }

    def pantalla_actual(self):
        """Devuelve la pantalla asociada al estado actual."""
        return self.pantallas[self.estado]

    def cambiar_estado(self, nuevo_estado):
        """Aplica un cambio de pantalla desde un único lugar."""
        if nuevo_estado is None or nuevo_estado == self.estado:
            return

        if nuevo_estado == EstadoJuego.JUEGO and self.estado in (
            EstadoJuego.MENU,
            EstadoJuego.FINAL,
        ):
            self.reiniciar_partida()

        self.estado = nuevo_estado
        self.opcion_menu = 0
        self._actualizar_audio()

    def reiniciar_partida(self):
        """Deja la partida en su estado inicial y limpia los datos previos."""
        self.nivel_actual = 0
        self.vidas = VIDAS_INICIALES
        self.puntaje = 0
        self.puntaje_final = 0
        self.texto_nombre = ""
        self.mensaje_nombre = ""
        self.mensaje_resultado = ""
        self.cargar_nivel(0)

    def cargar_nivel(self, nivel):
        """Carga un nivel en la pantalla de juego."""
        self.nivel_actual = nivel
        self.pantallas[EstadoJuego.JUEGO].cargar_nivel(nivel)

    def cargar_ranking(self):
        """Vuelve a leer el ranking desde la base de datos."""
        self.database.cargar_ranking()

    def manejar_eventos(self):
        """Distribuye cada evento a la pantalla actual."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.salir()

            if (
                event.type == pygame.KEYDOWN
                and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
                and (getattr(event, "mod", 0) & pygame.KMOD_ALT)
            ):
                self.toggle_fullscreen()
                continue

            nuevo_estado = self.pantalla_actual().handle_event(self, event)
            self.cambiar_estado(nuevo_estado)

    def toggle_fullscreen(self):
        """Alterna entre modo ventana y pantalla completa."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            try:
                ancho, alto = pygame.display.get_desktop_sizes()[0]
            except (AttributeError, IndexError):
                info = pygame.display.Info()
                ancho, alto = info.current_w, info.current_h
            self.display = pygame.display.set_mode(
                (ancho, alto), pygame.FULLSCREEN
            )
        else:
            self.display = pygame.display.set_mode(
                (ANCHO_PANTALLA, ALTO_PANTALLA)
            )

    def presentar(self):
        """Muestra la superficie del juego, escalada si está en pantalla completa."""
        if self.fullscreen:
            dw, dh = self.display.get_size()
            sw, sh = self.pantalla.get_size()
            scale = min(dw / sw, dh / sh)
            tw, th = int(sw * scale), int(sh * scale)
            x = (dw - tw) // 2
            y = (dh - th) // 2
            self.display.fill((0, 0, 0))
            scaled = pygame.transform.scale(self.pantalla, (tw, th))
            self.display.blit(scaled, (x, y))
        else:
            self.display.blit(self.pantalla, (0, 0))
        pygame.display.flip()

    def _actualizar_audio(self):
        if self.estado == EstadoJuego.JUEGO:
            self.audio.reproducir_musica("maze_lv1")
        else:
            self.audio.detener_pasos()
            self.audio.reproducir_musica("menu_sound")

    def actualizar(self, dt):
        """Actualiza la pantalla actual y aplica el estado que devuelva."""
        pantalla = self.pantalla_actual()
        actualizar = getattr(pantalla, "update", None)
        if actualizar:
            nuevo_estado = actualizar(self, dt)
            self.cambiar_estado(nuevo_estado)

    def dibujar(self):
        """Dibuja la pantalla actual."""
        self.pantalla_actual().draw(self)

    def ejecutar(self):
        """Ejecuta el bucle principal hasta que el jugador salga."""
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.manejar_eventos()
            self.actualizar(dt)
            self.dibujar()
            self.presentar()

    def salir(self):
        """Cierra pygame y termina el proceso."""
        pygame.quit()
        sys.exit()
