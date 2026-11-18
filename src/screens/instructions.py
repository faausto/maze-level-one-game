"""Pantalla de instrucciones del juego."""

import pygame

from src.constants import (
    ANCHO_PANTALLA,
    COLOR_DORADO,
    COLOR_DORADO_CLARO,
    COLOR_PANEL_OSCURO,
    COLOR_TEXTO,
    VIDAS_INICIALES,
)
from src.estados import EstadoJuego
from src.ui import fonts
from src.ui.background import dibujar_fondo_general
from src.ui.common import dibujar_panel, dibujar_separador, render_con_borde


class InstructionsScreen:
    """Muestra los controles y las reglas básicas del juego."""

    def handle_event(self, game, event):
        """Vuelve al menú al presionar ESC."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return EstadoJuego.MENU
        return None

    def draw(self, game):
        """Dibuja la lista de instrucciones."""
        pantalla = game.pantalla
        dibujar_fondo_general(pantalla, oscurecer=85)

        self._dibujar_titulo(pantalla)
        self._dibujar_panel(pantalla)
        self._dibujar_lineas(pantalla)

    def _dibujar_titulo(self, pantalla):
        """Dibuja el título y su separador."""
        titulo = render_con_borde(
            fonts.fuente_titulo_pantalla, "Instrucciones", COLOR_DORADO
        )
        pantalla.blit(
            titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 58)
        )
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            58 + titulo.get_height() + 8,
            320,
            COLOR_DORADO,
        )

    def _dibujar_panel(self, pantalla):
        """Dibuja el panel que contiene las instrucciones."""
        panel = pygame.Rect(150, 188, 724, 510)
        dibujar_panel(
            pantalla,
            panel,
            (*COLOR_PANEL_OSCURO, 180),
            COLOR_DORADO,
            2,
            18,
            COLOR_DORADO_CLARO,
        )

    def _dibujar_lineas(self, pantalla):
        """Dibuja cada línea de instrucciones."""
        instrucciones = [
            "Controles: W A S D o flechas",
            "Objetivo: encuentra la salida del laberinto",
            "Cada fruta vale 10 puntos",
            "Evita los monstruos",
            "Junta 3 frutas en 10 s: inmunidad",
            f"Tienes {VIDAS_INICIALES} vidas por partida",
            "Completa los niveles antes del tiempo",
            "Pantalla completa o ventana: Alt + Enter",
            "",
            "Presiona ESC para volver",
        ]
        for i, linea in enumerate(instrucciones):
            if not linea:
                continue
            color = COLOR_DORADO_CLARO if "ESC" in linea else COLOR_TEXTO
            texto = render_con_borde(
                fonts.fuente_texto_pantalla, linea, color, grosor=1
            )
            pantalla.blit(
                texto,
                (ANCHO_PANTALLA // 2 - texto.get_width() // 2, 234 + i * 48),
            )
