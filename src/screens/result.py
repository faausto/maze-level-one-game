"""Pantalla de resultado de la partida."""

import pygame

from src.constants import (
    ANCHO_PANTALLA,
    COLOR_BORDE_DERROTA,
    COLOR_DERROTA,
    COLOR_DERROTA_CLARO,
    COLOR_DORADO,
    COLOR_DORADO_CLARO,
    COLOR_FONDO,
    COLOR_PANEL_DERROTA,
    COLOR_TEXTO,
)
from src.estados import EstadoJuego
from src.ui import fonts
from src.ui.background import dibujar_fondo_gameover
from src.ui.common import dibujar_panel, dibujar_separador, render_con_borde


class ResultScreen:
    """Muestra si la partida terminó en victoria o en Game Over."""

    def handle_event(self, game, event):
        """Continúa a la pantalla final al presionar ENTER."""
        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_RETURN,
            pygame.K_KP_ENTER,
        ):
            game.audio.reproducir("menu_confirm")
            game.opcion_menu = 0
            return EstadoJuego.FINAL
        return None

    def draw(self, game):
        """Dibuja el resultado de la partida."""
        if "victoria" in game.mensaje_resultado.lower():
            self._dibujar_victoria(game)
        else:
            self._dibujar_derrota(game)

    def _dibujar_victoria(self, game):
        """Dibuja el resultado de victoria."""
        pantalla = game.pantalla
        pantalla.fill(COLOR_FONDO)

        titulo = render_con_borde(
            fonts.fuente_titulo_pantalla,
            game.mensaje_resultado,
            COLOR_DORADO,
        )
        pantalla.blit(
            titulo,
            (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 192),
        )
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            192 + titulo.get_height() + 8,
            300,
            COLOR_DORADO,
        )
        self._dibujar_puntaje(pantalla, game.puntaje_final, COLOR_TEXTO, 320)
        self._dibujar_ayuda(pantalla, COLOR_DORADO_CLARO, 448)

    def _dibujar_derrota(self, game):
        """Dibuja el resultado de derrota."""
        pantalla = game.pantalla
        dibujar_fondo_gameover(pantalla, oscurecer=120)

        panel = pygame.Rect(182, 150, 660, 430)
        dibujar_panel(
            pantalla,
            panel,
            (*COLOR_PANEL_DERROTA, 205),
            COLOR_DERROTA,
            2,
            20,
            COLOR_BORDE_DERROTA,
            sombra=10,
        )
        self._dibujar_titulo_derrota(pantalla, panel)
        self._dibujar_subtitulo(pantalla)
        self._dibujar_puntaje(pantalla, game.puntaje_final, COLOR_TEXTO, 458)
        self._dibujar_ayuda(pantalla, COLOR_DERROTA_CLARO, 524)

    def _dibujar_titulo_derrota(self, pantalla, panel):
        """Dibuja el título y el separador de la derrota."""
        titulo = render_con_borde(
            fonts.fuente_titulo_derrota,
            "DERROTA",
            COLOR_DERROTA,
            (6, 3, 6),
            grosor=4,
        )
        y_titulo = panel.y + 24
        pantalla.blit(
            titulo,
            (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, y_titulo),
        )
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            y_titulo + titulo.get_height() + 8,
            340,
            COLOR_BORDE_DERROTA,
        )

    def _dibujar_subtitulo(self, pantalla):
        """Dibuja el subtítulo de la derrota."""
        subtitulo = render_con_borde(
            fonts.fuente_texto_pantalla,
            "La oscuridad te alcanzó en el laberinto...",
            COLOR_DERROTA_CLARO,
            grosor=1,
        )
        pantalla.blit(
            subtitulo,
            (ANCHO_PANTALLA // 2 - subtitulo.get_width() // 2, 400),
        )

    def _dibujar_puntaje(self, pantalla, puntaje, color, y):
        """Dibuja el puntaje final en la posición indicada."""
        texto_puntaje = render_con_borde(
            fonts.fuente_texto_pantalla,
            f"Puntaje final: {puntaje}",
            color,
            grosor=1,
        )
        pantalla.blit(
            texto_puntaje,
            (ANCHO_PANTALLA // 2 - texto_puntaje.get_width() // 2, y),
        )

    def _dibujar_ayuda(self, pantalla, color, y):
        """Dibuja la ayuda de continuación en la posición indicada."""
        texto_opcion = render_con_borde(
            fonts.fuente_texto_pantalla_pequena,
            "Presiona ENTER para continuar",
            color,
            grosor=1,
        )
        pantalla.blit(
            texto_opcion,
            (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, y),
        )
