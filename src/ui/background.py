import os
import pygame
from src.constants import ANCHO_PANTALLA, ALTO_PANTALLA, COLOR_FONDO

_DIRECTORIO_FONDOS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "assets",
    "images",
    "background",
)
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
            ruta = os.path.join(_DIRECTORIO_FONDOS, nombre_archivo)
            imagen = pygame.image.load(ruta).convert()
            _fondos[nombre_archivo] = _escalar_cubriendo(
                imagen, ANCHO_PANTALLA, ALTO_PANTALLA
            )
        except Exception as e:
            print(f"Error cargando fondo {nombre_archivo}: {e}")
            _fondos[nombre_archivo] = None
    return _fondos[nombre_archivo]


def cargar_fondo_general():
    return _cargar_fondo("general_background.png")


def cargar_fondo_gameover():
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
    _dibujar_fondo(pantalla, cargar_fondo_general(), (8, 13, 8), oscurecer)


def dibujar_fondo_gameover(pantalla, oscurecer=110):
    _dibujar_fondo(pantalla, cargar_fondo_gameover(), (6, 8, 18), oscurecer)
