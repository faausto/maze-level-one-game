import pygame
from src.constants import COLOR_FONDO, COLOR_TEXTO, COLOR_TITULO, ANCHO_PANTALLA
from src.ui import fonts


class InstructionsScreen:
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game.estado = game.estado_juego.MENU

    def draw(self, game):
        pantalla = game.pantalla
        pantalla.fill(COLOR_FONDO)
        titulo = fonts.fuente_titulo.render("Instrucciones", True, COLOR_TITULO)
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 80))

        instrucciones = [
            "Controles: W A S D o flechas",
            "Objetivo: encuentra la salida del laberinto",
            "Recolecta frutas para sumar puntos",
            "Evita los monstruos",
            "Tienes 5 vidas por partida",
            "Completa los niveles antes del tiempo",
            "",
            "Presiona ESC para volver",
        ]
        for i, linea in enumerate(instrucciones):
            texto = fonts.fuente.render(linea, True, COLOR_TEXTO)
            pantalla.blit(texto, (ANCHO_PANTALLA // 2 - texto.get_width() // 2, 200 + i * 45))

        pygame.display.flip()
