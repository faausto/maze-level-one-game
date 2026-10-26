import pygame
from src.constants import (
    COLOR_HUD,
    COLOR_BORDE,
    COLOR_TEXTO,
    COLOR_TITULO,
    ANCHO_PANTALLA,
)
from src.ui import fonts


def dibujar_hud(pantalla, vidas, puntaje, tiempo_nivel, nivel_actual, inmune):
    panel = pygame.Rect(0, 0, ANCHO_PANTALLA, 80)
    pygame.draw.rect(pantalla, COLOR_HUD, panel)
    pygame.draw.line(pantalla, COLOR_BORDE, (0, 80), (ANCHO_PANTALLA, 80), 2)

    info_vidas = fonts.fuente.render(f"Vidas: {vidas}", True, COLOR_TITULO)
    info_puntos = fonts.fuente.render(f"Puntos: {puntaje}", True, COLOR_TEXTO)
    info_tiempo = fonts.fuente.render(f"Tiempo: {int(tiempo_nivel)}", True, COLOR_TEXTO)
    info_nivel = fonts.fuente.render(f"Nivel: {nivel_actual + 1}", True, COLOR_TEXTO)

    pantalla.blit(info_vidas, (20, 20))
    pantalla.blit(info_puntos, (200, 20))
    pantalla.blit(info_tiempo, (400, 20))
    pantalla.blit(info_nivel, (600, 20))

    if inmune:
        texto_inmune = fonts.fuente_pequena.render("INMUNE", True, (0, 255, 0))
        pantalla.blit(texto_inmune, (ANCHO_PANTALLA - 120, 20))
