"""Carga y dibujo de los fondos de las pantallas."""

import logging

import pygame

from src.constants import ALTO_PANTALLA, ANCHO_PANTALLA, COLOR_FONDO, IMAGES_DIR

logger = logging.getLogger(__name__)

_DIRECTORIO_FONDOS = IMAGES_DIR / "background"
_fondos = {}
_velos = {}


def _escalar_cubriendo(imagen, ancho, alto):
    ancho_img, alto_img = imagen.get_size()
    escala = max(ancho / ancho_img, alto / alto_img)
    nuevo_ancho = max(1, int(ancho_img * escala))
    nuevo_alto = max(1, int(alto_img * escala))
    escalada = pygame.transform.smoothscale(imagen, (nuevo_ancho, nuevo_alto))
    x = (nuevo_ancho - ancho) // 2
    y = (nuevo_alto - alto) // 2
    return escalada.subsurface(pygame.Rect(x, y, ancho, alto)).copy()


def _cargar_fondo(nombre_archivo):
    if nombre_archivo not in _fondos:
        try:
            imagen = pygame.image.load(
                _DIRECTORIO_FONDOS / nombre_archivo
            ).convert()
            _fondos[nombre_archivo] = _escalar_cubriendo(
                imagen, ANCHO_PANTALLA, ALTO_PANTALLA
            )
        except (pygame.error, OSError) as error:
            logger.warning("No se pudo cargar el fondo %s: %s", nombre_archivo, error)
            _fondos[nombre_archivo] = None
    return _fondos[nombre_archivo]


def cargar_fondo_general():
    """Devuelve el fondo general escalado a la pantalla."""
    return _cargar_fondo("general_background.png")


def cargar_fondo_gameover():
    """Devuelve el fondo de Game Over escalado a la pantalla."""
    return _cargar_fondo("gameover_background.png")


def _dibujar_fondo(pantalla, fondo, tono_velo, oscurecer):
    if fondo:
        pantalla.blit(fondo, (0, 0))
        if oscurecer > 0:
            clave = (tono_velo, oscurecer)
            if clave not in _velos:
                velo = pygame.Surface(
                    (ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA
                )
                velo.fill((*tono_velo, oscurecer))
                _velos[clave] = velo
            pantalla.blit(_velos[clave], (0, 0))
    else:
        pantalla.fill(COLOR_FONDO)


def dibujar_fondo_general(pantalla, oscurecer=80):
    """Dibuja el fondo general con un velo opcional."""
    _dibujar_fondo(pantalla, cargar_fondo_general(), (8, 13, 8), oscurecer)


def dibujar_fondo_gameover(pantalla, oscurecer=110):
    """Dibuja el fondo de Game Over con un velo opcional."""
    _dibujar_fondo(pantalla, cargar_fondo_gameover(), (6, 8, 18), oscurecer)
