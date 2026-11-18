"""Pantalla del menú principal."""

import logging

import pygame

from src.constants import ALTO_PANTALLA, ANCHO_PANTALLA, COLOR_FONDO, IMAGES_DIR
from src.estados import EstadoJuego
from src.ui.menu_ui import dibujar_opciones_menu

logger = logging.getLogger(__name__)


class MenuScreen:
    """Menú principal con las opciones de jugar, instrucciones, ranking y salir."""

    _background = None

    def __init__(self):
        if MenuScreen._background is None:
            self._cargar_fondo()

    def _cargar_fondo(self):
        try:
            img = pygame.image.load(
                IMAGES_DIR / "background" / "menu_background.png"
            ).convert()
            MenuScreen._background = pygame.transform.scale(
                img, (ANCHO_PANTALLA, ALTO_PANTALLA)
            )
        except (pygame.error, OSError) as error:
            logger.warning("No se pudo cargar el fondo del menú: %s", error)
            MenuScreen._background = None

    def handle_event(self, game, event):
        """Navega el menú y devuelve el próximo estado, o None."""
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_UP:
            game.opcion_menu = (game.opcion_menu - 1) % len(game.opciones_menu)
            game.audio.reproducir("menu_select")
        elif event.key == pygame.K_DOWN:
            game.opcion_menu = (game.opcion_menu + 1) % len(game.opciones_menu)
            game.audio.reproducir("menu_select")
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            game.audio.reproducir("menu_confirm")
            if game.opcion_menu == 0:
                return EstadoJuego.JUEGO
            if game.opcion_menu == 1:
                return EstadoJuego.INSTRUCCIONES
            if game.opcion_menu == 2:
                game.cargar_ranking()
                return EstadoJuego.RANKING
            if game.opcion_menu == 3:
                game.salir()
        return None

    def draw(self, game):
        """Dibuja el fondo y las opciones del menú."""
        pantalla = game.pantalla
        if MenuScreen._background:
            pantalla.blit(MenuScreen._background, (0, 0))
        else:
            pantalla.fill(COLOR_FONDO)

        dibujar_opciones_menu(pantalla, game.opciones_menu, game.opcion_menu)
