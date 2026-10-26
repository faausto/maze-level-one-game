import pygame
from src.constants import (
    COLOR_FONDO,
    COLOR_PANEL,
    COLOR_BORDE,
    COLOR_TEXTO,
    COLOR_TITULO,
    ANCHO_PANTALLA,
)
from src.ui import fonts


def dibujar_opciones_menu(pantalla, opciones, opcion_seleccionada):
    for i, opcion in enumerate(opciones):
        color = COLOR_TITULO if i == opcion_seleccionada else COLOR_TEXTO
        texto = fonts.fuente.render(opcion, True, color)
        pantalla.blit(texto, (ANCHO_PANTALLA // 2 - texto.get_width() // 2, 250 + i * 60))
