"""Pantalla de ingreso del nombre para el ranking."""

import pygame

from src.constants import (
    ANCHO_PANTALLA,
    COLOR_DERROTA_CLARO,
    COLOR_DORADO,
    COLOR_DORADO_CLARO,
    COLOR_FONDO,
    COLOR_PANEL_OSCURO,
    COLOR_TEXTO,
)
from src.estados import EstadoJuego
from src.ui import fonts
from src.ui.common import dibujar_panel, dibujar_separador, render_con_borde


class NameInputScreen:
    """Pide el nombre del jugador antes de guardar el puntaje en el ranking."""

    def handle_event(self, game, event):
        """Edita el nombre y devuelve el próximo estado, o None."""
        if event.type != pygame.KEYDOWN:
            return None

        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            nombre = game.texto_nombre.strip()
            if not nombre:
                return None
            game.audio.reproducir("menu_confirm")
            if game.database.guardar_puntaje(nombre, game.puntaje_final):
                game.mensaje_nombre = ""
                game.cargar_ranking()
                game.opcion_menu = 0
                return EstadoJuego.RANKING_VICTORIA
            game.mensaje_nombre = "No se pudo guardar el puntaje. Intenta de nuevo."
        elif event.key == pygame.K_BACKSPACE:
            game.texto_nombre = game.texto_nombre[:-1]
            game.mensaje_nombre = ""
        elif event.key == pygame.K_ESCAPE:
            return EstadoJuego.FINAL
        elif len(game.texto_nombre) < 15 and event.unicode.isprintable():
            game.texto_nombre += event.unicode
            game.mensaje_nombre = ""
        return None

    def draw(self, game):
        """Dibuja el puntaje, el campo de nombre y los avisos."""
        pantalla = game.pantalla
        pantalla.fill(COLOR_FONDO)

        self._dibujar_titulo(pantalla)
        self._dibujar_panel_puntaje(pantalla, game.puntaje_final)
        self._dibujar_campo_nombre(pantalla, game.texto_nombre)
        self._dibujar_aviso(pantalla, game.mensaje_nombre)
        self._dibujar_ayuda(pantalla)

    def _dibujar_titulo(self, pantalla):
        """Dibuja el título de victoria y su separador."""
        titulo = render_con_borde(
            fonts.fuente_titulo_pantalla, "Victoria!", COLOR_DORADO
        )
        pantalla.blit(
            titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 130)
        )
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            130 + titulo.get_height() + 8,
            300,
            COLOR_DORADO,
        )

    def _dibujar_panel_puntaje(self, pantalla, puntaje):
        """Dibuja el panel con el puntaje final."""
        texto_puntaje = render_con_borde(
            fonts.fuente_puntaje_final,
            f"Puntaje final: {puntaje}",
            COLOR_DORADO_CLARO,
            grosor=2,
        )
        ancho_puntaje = max(420, texto_puntaje.get_width() + 64)
        panel_puntaje = pygame.Rect(
            ANCHO_PANTALLA // 2 - ancho_puntaje // 2, 236, ancho_puntaje, 72
        )
        dibujar_panel(
            pantalla,
            panel_puntaje,
            (*COLOR_PANEL_OSCURO, 180),
            COLOR_DORADO,
            2,
            16,
            COLOR_DORADO_CLARO,
            sombra=6,
        )
        pantalla.blit(
            texto_puntaje,
            (
                panel_puntaje.centerx - texto_puntaje.get_width() // 2,
                panel_puntaje.centery - texto_puntaje.get_height() // 2,
            ),
        )

    def _dibujar_campo_nombre(self, pantalla, nombre):
        """Dibuja la etiqueta y el campo de ingreso del nombre."""
        texto = render_con_borde(
            fonts.fuente_texto_pantalla,
            "Ingresa tu nombre:",
            COLOR_TEXTO,
            grosor=1,
        )
        pantalla.blit(
            texto, (ANCHO_PANTALLA // 2 - texto.get_width() // 2, 340)
        )

        input_rect = pygame.Rect(ANCHO_PANTALLA // 2 - 200, 388, 400, 64)
        dibujar_panel(
            pantalla,
            input_rect,
            (*COLOR_PANEL_OSCURO, 170),
            COLOR_DORADO,
            2,
            12,
            COLOR_DORADO_CLARO,
        )
        texto_nombre = fonts.fuente_texto_pantalla.render(
            nombre or "_", True, COLOR_TEXTO
        )
        pantalla.blit(texto_nombre, (input_rect.x + 16, input_rect.y + 16))

    def _dibujar_aviso(self, pantalla, mensaje):
        """Dibuja el mensaje de error, si hay uno."""
        if not mensaje:
            return
        aviso = render_con_borde(
            fonts.fuente_texto_pantalla_pequena,
            mensaje,
            COLOR_DERROTA_CLARO,
            grosor=1,
        )
        pantalla.blit(
            aviso,
            (ANCHO_PANTALLA // 2 - aviso.get_width() // 2, 466),
        )

    def _dibujar_ayuda(self, pantalla):
        """Dibuja la ayuda de guardado."""
        texto_opcion = render_con_borde(
            fonts.fuente_texto_pantalla_pequena,
            "Presiona ENTER para guardar",
            COLOR_DORADO_CLARO,
            grosor=1,
        )
        pantalla.blit(
            texto_opcion,
            (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 510),
        )
