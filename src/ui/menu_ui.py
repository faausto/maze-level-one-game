"""Dibujo compartido de las opciones de menú."""

import pygame

from src.constants import (
    ALTO_OPCION,
    ANCHO_OPCION,
    ANCHO_PANTALLA,
    ESPACIO_OPCIONES,
    RADIO_OPCION,
    Y_INICIAL_OPCIONES,
)
from src.ui import fonts
from src.ui.common import dibujar_panel, render_con_borde

COLOR_TEXTO_BORDE = (12, 16, 10)
COLOR_TEXTO_NORMAL = (240, 240, 228)
COLOR_TEXTO_SELECCION = (255, 232, 140)

COLOR_PANEL_SELECCION = (58, 44, 18, 210)
COLOR_BORDE_SELECCION = (255, 214, 92)
COLOR_BORDE_INTERNO = (255, 248, 205)
COLOR_BRILLO = (255, 210, 90)

_cache_texto = {}


def _texto_opcion(texto, seleccionado):
    clave = (texto, seleccionado)
    if clave not in _cache_texto:
        color = COLOR_TEXTO_SELECCION if seleccionado else COLOR_TEXTO_NORMAL
        _cache_texto[clave] = render_con_borde(
            fonts.fuente_menu, texto, color, COLOR_TEXTO_BORDE
        )
    return _cache_texto[clave]


def _dibujar_brillo(pantalla, rect):
    pad = 18
    brillo = pygame.Surface(
        (rect.width + pad * 2, rect.height + pad * 2), pygame.SRCALPHA
    )
    for i in range(pad, 0, -1):
        alpha = max(8, 28 - i)
        halo = pygame.Rect(
            pad - i, pad - i, rect.width + i * 2, rect.height + i * 2
        )
        pygame.draw.rect(
            brillo, (*COLOR_BRILLO, alpha), halo, border_radius=RADIO_OPCION + i
        )
    pantalla.blit(brillo, (rect.x - pad, rect.y - pad))


def _dibujar_panel_seleccion(pantalla, rect):
    _dibujar_brillo(pantalla, rect)
    dibujar_panel(
        pantalla,
        rect,
        COLOR_PANEL_SELECCION,
        COLOR_BORDE_SELECCION,
        3,
        RADIO_OPCION,
        COLOR_BORDE_INTERNO,
    )


def dibujar_opciones_menu(pantalla, opciones, opcion_seleccionada):
    """Dibuja las opciones y resalta la elegida con un panel alineado al texto."""
    textos = [
        _texto_opcion(opcion, i == opcion_seleccionada)
        for i, opcion in enumerate(opciones)
    ]
    ancho_opcion = max(ANCHO_OPCION, max(t.get_width() for t in textos) + 56)

    for i, texto in enumerate(textos):
        seleccionado = i == opcion_seleccionada

        y_texto = Y_INICIAL_OPCIONES + i * ESPACIO_OPCIONES
        x_texto = ANCHO_PANTALLA // 2 - texto.get_width() // 2
        centro_y = y_texto + texto.get_height() // 2

        rect = pygame.Rect(
            ANCHO_PANTALLA // 2 - ancho_opcion // 2,
            centro_y - ALTO_OPCION // 2,
            ancho_opcion,
            ALTO_OPCION,
        )

        if seleccionado:
            _dibujar_panel_seleccion(pantalla, rect)
        pantalla.blit(texto, (x_texto, y_texto))
