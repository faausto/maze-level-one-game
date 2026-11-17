import pygame
from src.constants import (
    ANCHO_PANTALLA,
    COLOR_DORADO,
    COLOR_DORADO_CLARO,
    COLOR_PANEL_OSCURO,
    COLOR_TEXTO,
)
from src.ui import fonts
from src.ui.background import dibujar_fondo_general
from src.ui.common import dibujar_panel, dibujar_separador, render_con_borde


class InstructionsScreen:
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game.estado = game.estado_juego.MENU

    def draw(self, game):
        pantalla = game.pantalla
        dibujar_fondo_general(pantalla, oscurecer=85)

        titulo = render_con_borde(
            fonts.fuente_titulo_pantalla, "Instrucciones", COLOR_DORADO
        )
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 58))
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            58 + titulo.get_height() + 8,
            320,
            COLOR_DORADO,
        )

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

        instrucciones = [
            "Controles: W A S D o flechas",
            "Objetivo: encuentra la salida del laberinto",
            "Recolecta frutas para sumar puntos",
            "Evita los monstruos",
            "Tienes 5 vidas por partida",
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
