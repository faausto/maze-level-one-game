"""Pantalla final de victoria o derrota."""

import pygame

from src.constants import (
    ANCHO_PANTALLA,
    COLOR_BORDE_DERROTA,
    COLOR_DERROTA,
    COLOR_DERROTA_CLARO,
    COLOR_DORADO,
    COLOR_DORADO_CLARO,
    COLOR_PANEL_DERROTA,
    COLOR_PANEL_OSCURO,
    COLOR_TEXTO,
)
from src.estados import EstadoJuego
from src.ui import fonts
from src.ui.background import dibujar_fondo_gameover, dibujar_fondo_general
from src.ui.common import dibujar_panel, dibujar_separador, render_con_borde
from src.ui.menu_ui import dibujar_opciones_menu


class FinalScreen:
    """Pantalla final con el puntaje y las opciones de continuar."""

    def handle_event(self, game, event):
        """Navega las opciones finales y devuelve el próximo estado, o None."""
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_UP:
            game.opcion_menu = (game.opcion_menu - 1) % 2
            game.audio.reproducir("menu_select")
        elif event.key == pygame.K_DOWN:
            game.opcion_menu = (game.opcion_menu + 1) % 2
            game.audio.reproducir("menu_select")
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            game.audio.reproducir("menu_confirm")
            if game.opcion_menu == 0:
                return EstadoJuego.JUEGO
            return EstadoJuego.MENU
        return None

    def draw(self, game):
        """Dibuja la pantalla final según el resultado de la partida."""
        es_victoria = "victoria" in game.mensaje_resultado.lower()
        estilo = self._estilo_final(game, es_victoria)

        self._dibujar_panel_final(game.pantalla, estilo)
        self._dibujar_encabezado(game.pantalla, estilo)
        self._dibujar_puntaje(game.pantalla, game, estilo)

        opciones = ["Jugar de nuevo", "Volver al menu principal"]
        dibujar_opciones_menu(game.pantalla, opciones, game.opcion_menu)
        self._dibujar_ayuda(game.pantalla, estilo["color_ayuda"])

    def _estilo_final(self, game, es_victoria):
        """Dibuja el fondo y devuelve los colores y textos del resultado."""
        if es_victoria:
            dibujar_fondo_general(game.pantalla, oscurecer=80)
            return {
                "relleno": (*COLOR_PANEL_OSCURO, 185),
                "borde": COLOR_DORADO,
                "borde_interno": COLOR_DORADO_CLARO,
                "color_titulo": COLOR_DORADO,
                "color_separador": COLOR_DORADO,
                "color_puntaje": COLOR_DORADO_CLARO,
                "color_ayuda": COLOR_DORADO_CLARO,
                "texto_titulo": game.mensaje_resultado,
                "fuente_titulo": fonts.fuente_titulo_pantalla,
                "y_titulo": 100,
                "y_puntaje": 240,
                "grosor": 2,
                "sombra_titulo": (10, 12, 8),
            }

        dibujar_fondo_gameover(game.pantalla, oscurecer=110)
        return {
            "relleno": (*COLOR_PANEL_DERROTA, 205),
            "borde": COLOR_DERROTA,
            "borde_interno": COLOR_BORDE_DERROTA,
            "color_titulo": COLOR_DERROTA,
            "color_separador": COLOR_BORDE_DERROTA,
            "color_puntaje": COLOR_TEXTO,
            "color_ayuda": COLOR_DERROTA_CLARO,
            "texto_titulo": "DERROTA",
            "fuente_titulo": fonts.fuente_titulo_derrota,
            "y_titulo": 82,
            "y_puntaje": 250,
            "grosor": 4,
            "sombra_titulo": (6, 3, 6),
        }

    def _dibujar_panel_final(self, pantalla, estilo):
        """Dibuja el panel que contiene el resultado."""
        panel = pygame.Rect(192, 70, 640, 610)
        dibujar_panel(
            pantalla,
            panel,
            estilo["relleno"],
            estilo["borde"],
            2,
            20,
            estilo["borde_interno"],
            sombra=8,
        )

    def _dibujar_encabezado(self, pantalla, estilo):
        """Dibuja el título y el separador del resultado."""
        titulo = render_con_borde(
            estilo["fuente_titulo"],
            estilo["texto_titulo"],
            estilo["color_titulo"],
            estilo["sombra_titulo"],
            grosor=estilo["grosor"],
        )
        y_titulo = estilo["y_titulo"]
        pantalla.blit(
            titulo,
            (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, y_titulo),
        )
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            y_titulo + titulo.get_height() + 8,
            300,
            estilo["color_separador"],
        )

    def _dibujar_puntaje(self, pantalla, game, estilo):
        """Dibuja el puntaje final de la partida."""
        texto_puntaje = render_con_borde(
            fonts.fuente_puntaje_final,
            f"Puntaje final: {game.puntaje_final}",
            estilo["color_puntaje"],
            grosor=2,
        )
        pantalla.blit(
            texto_puntaje,
            (
                ANCHO_PANTALLA // 2 - texto_puntaje.get_width() // 2,
                estilo["y_puntaje"],
            ),
        )

    def _dibujar_ayuda(self, pantalla, color):
        """Dibuja la ayuda de navegación al pie del panel."""
        texto_opcion = render_con_borde(
            fonts.fuente_texto_pantalla_pequena,
            "Usa las flechas y ENTER para elegir",
            color,
            grosor=1,
        )
        pantalla.blit(
            texto_opcion,
            (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 610),
        )
