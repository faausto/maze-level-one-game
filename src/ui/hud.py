"""HUD con vidas, puntaje, tiempo y nivel."""

import pygame

from src.constants import (
    ANCHO_PANTALLA,
    COLOR_DORADO,
    COLOR_TEXTO,
    HUD_HEIGHT,
    VIDAS_INICIALES,
)
from src.ui import fonts
from src.ui.common import render_con_borde

_ANCHO_BARRA = 30
_ALTO_BARRA = 22
_SEPARACION_BARRA = 8
_X_VIDAS = 38
_Y_BARRA = 40

_X_PUNTOS = 262
_X_TIEMPO = 508
_X_NIVEL = 754
_Y_ETIQUETA = 12
_Y_VALOR = 40

_COLOR_ETIQUETA = COLOR_DORADO
_COLOR_VALOR = COLOR_TEXTO
_COLOR_BORDE_TEXTO = (10, 12, 8)

_hud_fondo = None


def _mezclar(color_a, color_b, t):
    return tuple(
        int(color_a[i] + (color_b[i] - color_a[i]) * t) for i in range(3)
    )


def _obtener_fondo_hud():
    global _hud_fondo
    if _hud_fondo is None:
        fondo = pygame.Surface((ANCHO_PANTALLA, HUD_HEIGHT))
        for y in range(HUD_HEIGHT):
            t = y / max(1, HUD_HEIGHT - 1)
            color = _mezclar((38, 50, 33), (20, 28, 18), t)
            pygame.draw.line(fondo, color, (0, y), (ANCHO_PANTALLA, y))
        pygame.draw.line(
            fondo, (64, 80, 52), (0, 0), (ANCHO_PANTALLA, 0), 1
        )
        _hud_fondo = fondo
    return _hud_fondo


def _dibujar_vidas(pantalla, vidas):
    vidas = max(0, min(VIDAS_INICIALES, int(vidas)))

    for i in range(VIDAS_INICIALES):
        x = _X_VIDAS + i * (_ANCHO_BARRA + _SEPARACION_BARRA)
        barra = pygame.Rect(x, _Y_BARRA, _ANCHO_BARRA, _ALTO_BARRA)

        pygame.draw.rect(
            pantalla, (12, 16, 10), barra.move(0, 2), border_radius=4
        )

        if i < vidas:
            pygame.draw.rect(pantalla, (104, 24, 23), barra, border_radius=4)
            interior = barra.inflate(-2, -2)
            pygame.draw.rect(pantalla, (196, 50, 44), interior, border_radius=3)
            brillo = pygame.Rect(
                barra.x + 4, barra.y + 3, barra.width - 8, 5
            )
            pygame.draw.rect(pantalla, (238, 112, 94), brillo, border_radius=2)
        else:
            pygame.draw.rect(pantalla, (34, 42, 29), barra, border_radius=4)
            pygame.draw.rect(
                pantalla, (62, 74, 50), barra, 1, border_radius=4
            )


def _dibujar_estadistica(pantalla, x, etiqueta, valor):
    texto_etiqueta = render_con_borde(
        fonts.fuente_hud_etiqueta,
        etiqueta,
        _COLOR_ETIQUETA,
        _COLOR_BORDE_TEXTO,
        grosor=1,
    )
    texto_valor = render_con_borde(
        fonts.fuente_hud_valor,
        str(valor),
        _COLOR_VALOR,
        _COLOR_BORDE_TEXTO,
        grosor=1,
    )

    pantalla.blit(texto_etiqueta, (x - 1, _Y_ETIQUETA - 1))
    pantalla.blit(texto_valor, (x - 1, _Y_VALOR - 1))


def dibujar_hud(pantalla, vidas, puntaje, tiempo_nivel, nivel_actual, inmune):
    """Dibuja la barra superior con el estado de la partida."""
    pantalla.blit(_obtener_fondo_hud(), (0, 0))

    pygame.draw.line(
        pantalla,
        (58, 72, 46),
        (0, HUD_HEIGHT),
        (ANCHO_PANTALLA, HUD_HEIGHT),
        2,
    )
    pygame.draw.line(
        pantalla,
        (122, 100, 52),
        (0, HUD_HEIGHT - 2),
        (ANCHO_PANTALLA, HUD_HEIGHT - 2),
        2,
    )

    for x in (240, 486, 732):
        pygame.draw.line(pantalla, (72, 86, 56), (x, 24), (x, 78), 1)

    _dibujar_vidas(pantalla, vidas)
    _dibujar_estadistica(pantalla, _X_PUNTOS, "PUNTOS", puntaje)
    _dibujar_estadistica(pantalla, _X_TIEMPO, "TIEMPO", int(tiempo_nivel))
    _dibujar_estadistica(pantalla, _X_NIVEL, "NIVEL", nivel_actual + 1)

    if inmune:
        texto_inmune = render_con_borde(
            fonts.fuente_hud_etiqueta,
            "INMUNE",
            (150, 255, 140),
            (8, 18, 8),
            grosor=1,
        )
        pantalla.blit(
            texto_inmune,
            (ANCHO_PANTALLA - 30 - texto_inmune.get_width(), 37),
        )
