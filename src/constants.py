"""Constantes de configuración y rutas de assets del proyecto."""

import os
import sys
from pathlib import Path

# --- Rutas ---
BASE_DIR = Path(__file__).resolve().parent.parent
CONGELADO = getattr(sys, "frozen", False)

if CONGELADO:
    # En el exe de PyInstaller los assets se extraen a una carpeta temporal.
    RECURSOS_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))
    DATOS_USUARIO_DIR = (
        Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        / "MazeLevelOneGame"
    )
else:
    RECURSOS_DIR = BASE_DIR
    DATOS_USUARIO_DIR = BASE_DIR / "database"

ASSETS_DIR = RECURSOS_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
DATABASE_DIR = DATOS_USUARIO_DIR

# --- Pantalla ---
ANCHO_PANTALLA, ALTO_PANTALLA = 1024, 768
FPS = 60
HUD_HEIGHT = 102

# --- Mundo y jugador ---
TILE_SIZE = 77
VELOCIDAD_JUGADOR = 384
VIDAS_INICIALES = 5
DURACION_INVULNERABILIDAD = 1.0  # segundos

# --- Monstruos ---
VELOCIDAD_MONSTRUO_NIVEL_1 = 154
VELOCIDAD_MONSTRUO_NIVEL_2 = int(VELOCIDAD_MONSTRUO_NIVEL_1 * 1.10)  # +10 %
RANGO_DETECCION_NIVEL_2 = 4 * TILE_SIZE  # 4 bloques = 308 px
PAUSA_MONSTRUO_TRAS_DANO = 0.6  # segundos detenido tras tocar al jugador
INTERVALO_RECALCULO_CAMINO = 0.25  # segundos entre BFS de persecución
DISTANCIA_MINIMA_SPAWN = 4 * TILE_SIZE  # frutas y monstruos lejos del spawn
PUNTOS_PATRULLA = 3  # puntos de patrulla además del spawn
RADIO_PATRULLA = 6  # celdas de distancia máxima para elegir la patrulla

# --- Inmunidad por frutas ---
FRUTAS_PARA_INMUNIDAD = 3
VENTANA_INMUNIDAD = 10  # segundos para juntar las frutas
DURACION_INMUNIDAD = 5  # segundos de inmunidad

# --- Puntajes (RF-16) ---
PUNTOS_POR_FRUTA = 10
BONUS_VICTORIA = 100
BONUS_POR_VIDA = 50
BONUS_POR_SEGUNDO = 5

# --- Menú ---
ANCHO_OPCION = 512
ALTO_OPCION = 62
ESPACIO_OPCIONES = 77
Y_INICIAL_OPCIONES = ALTO_PANTALLA * 5 // 12
RADIO_OPCION = 16

COLOR_FONDO = (75, 90, 60)
COLOR_CAMINO = (75, 90, 60)
COLOR_PARED = (60, 60, 80)
COLOR_BORDE_PARED = (90, 105, 70)
COLOR_BORDE_CAMINO = (65, 78, 50)
COLOR_PANEL = (55, 65, 45)
COLOR_HUD = (55, 65, 45)
COLOR_BORDE = (90, 105, 70)
COLOR_BOTON = (65, 78, 50)
COLOR_BOTON_HOVER = (85, 100, 65)
COLOR_TEXTO = (240, 235, 220)
COLOR_TITULO = (180, 230, 150)
COLOR_SELECCION = COLOR_TITULO
COLOR_JUGADOR = (0, 120, 255)
COLOR_OBJETIVO = (255, 80, 80)
COLOR_FRUTA = (255, 140, 0)
COLOR_SALIDA = (0, 255, 120)
COLOR_MONSTRUO = (200, 30, 30)

COLOR_DORADO = (255, 214, 92)
COLOR_DORADO_CLARO = (255, 238, 170)
COLOR_BORDE_DORADO = (176, 140, 60)
COLOR_PANEL_OSCURO = (18, 28, 18)
COLOR_PANEL_CREMA = (238, 230, 205)
COLOR_TEXTO_OSCURO = (55, 50, 35)

COLOR_DERROTA = (228, 62, 54)
COLOR_DERROTA_CLARO = (245, 150, 128)
COLOR_BORDE_DERROTA = (158, 52, 48)
COLOR_PANEL_DERROTA = (26, 18, 28)
