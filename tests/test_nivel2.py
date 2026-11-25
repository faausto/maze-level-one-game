"""Tests de la configuración del segundo nivel."""

from collections import deque
from itertools import pairwise

import pygame
import pytest

from src.constants import (
    PAUSA_MONSTRUO_TRAS_DANO,
    RANGO_DETECCION_NIVEL_2,
    TILE_SIZE,
    VELOCIDAD_JUGADOR,
    VELOCIDAD_MONSTRUO_NIVEL_1,
    VELOCIDAD_MONSTRUO_NIVEL_2,
)
from src.entities.monster import Monster
from src.screens.game_screen import GameScreen
from src.ui.hud import valores_tiempo
from src.world.maze import Maze
from src.world.seeds import (
    FRUTAS_POR_NIVEL,
    MONSTRUOS_POR_NIVEL,
    NIVELES,
    SEMILLAS,
)


def test_hay_dos_niveles_con_sus_tiempos():
    assert len(NIVELES) == 2
    assert NIVELES[0]["tiempo"] == 60
    assert NIVELES[1]["tiempo"] == 75


def test_nivel2_tiene_cinco_semillas_del_doble_tamano():
    filas_nivel1 = len(SEMILLAS[0][0])
    columnas_nivel1 = len(SEMILLAS[0][0][0])
    assert len(SEMILLAS[1]) == 5
    for mapa in SEMILLAS[1]:
        assert len(mapa) == 2 * filas_nivel1
        assert all(len(fila) == 2 * columnas_nivel1 for fila in mapa)


@pytest.mark.parametrize("indice", range(len(SEMILLAS[1])))
def test_nivel2_bordes_exteriores_de_un_bloque(indice):
    mapa = SEMILLAS[1][indice]
    assert set(mapa[0]) == {"1"}
    assert set(mapa[-1]) == {"1", "E"}
    assert all(fila[0] == "1" for fila in mapa)
    assert all(fila[-1] == "1" for fila in mapa)


@pytest.mark.parametrize("indice", range(len(SEMILLAS[1])))
def test_nivel2_sin_pasillos_de_dos_bloques(indice):
    mapa = SEMILLAS[1][indice]
    for y in range(len(mapa) - 1):
        for x in range(len(mapa[0]) - 1):
            cuadrado = {
                mapa[y][x],
                mapa[y][x + 1],
                mapa[y + 1][x],
                mapa[y + 1][x + 1],
            }
            assert "1" in cuadrado


def _buscar_celda(mapa, caracter):
    return next(
        (x, y)
        for y, fila in enumerate(mapa)
        for x, celda in enumerate(fila)
        if celda == caracter
    )


def _alcanzables(mapa, inicio, permitidas=None):
    alto, ancho = len(mapa), len(mapa[0])
    vistos = {inicio}
    cola = deque([inicio])
    while cola:
        x, y = cola.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < ancho and 0 <= ny < alto):
                continue
            if (nx, ny) in vistos or mapa[ny][nx] == "1":
                continue
            if permitidas is not None and (nx, ny) not in permitidas:
                continue
            vistos.add((nx, ny))
            cola.append((nx, ny))
    return vistos


def test_hud_nivel2_muestra_75_desde_el_inicio():
    # El tiempo total y el extra se descuentan por separado; hace falta
    # redondear hacia arriba para no mostrar 74 en el primer segundo.
    total = 75.0 + 10.0
    extra = 10.0
    for _ in range(60):
        assert valores_tiempo(total, extra) == (75, "+10")
        total -= 1 / 60
        extra -= 1 / 60


def test_hud_nivel2_corrige_error_de_punto_flotante():
    assert valores_tiempo(85.0, 10.0) == (75, "+10")
    assert valores_tiempo(74.99999999999999, 0) == (75, None)
    assert valores_tiempo(75.00000000000001, 0) == (75, None)
    assert valores_tiempo(75.0, 0) == (75, None)


@pytest.mark.parametrize("indice", range(len(SEMILLAS[1])))
def test_nivel2_el_anillo_perimetral_no_lleva_a_la_salida(indice):
    mapa = SEMILLAS[1][indice]
    alto, ancho = len(mapa), len(mapa[0])
    inicio = _buscar_celda(mapa, "S")
    destino = _buscar_celda(mapa, "E")
    anillo = (
        {(x, 1) for x in range(1, ancho - 1)}
        | {(x, alto - 2) for x in range(1, ancho - 1)}
        | {(1, y) for y in range(1, alto - 1)}
        | {(ancho - 2, y) for y in range(1, alto - 1)}
    )
    alcanzables = _alcanzables(mapa, inicio, anillo | {destino})
    assert destino not in alcanzables


def _el_centro_es_obligatorio(mapa, x0, x1, y0, y1):
    inicio = _buscar_celda(mapa, "S")
    destino = _buscar_celda(mapa, "E")
    centro = {
        (x, y)
        for y in range(y0, y1 + 1)
        for x in range(x0, x1 + 1)
        if mapa[y][x] != "1"
    }
    return destino not in _alcanzables(mapa, inicio, centro | {destino})


@pytest.mark.parametrize("indice", range(len(SEMILLAS[1])))
def test_nivel2_obliga_a_cruzar_el_centro(indice):
    # Bloquear el rectangulo central debe dejar la salida inalcanzable:
    # no puede existir una ruta que rodee el laberinto por los extremos.
    assert _el_centro_es_obligatorio(SEMILLAS[1][indice], 12, 27, 7, 18)


@pytest.mark.parametrize("indice", range(len(SEMILLAS[1])))
def test_nivel2_obliga_a_cruzar_el_nucleo_central(indice):
    # El cruce debe atravesar el nucleo estrecho, no solo acercarse
    # al borde del rectangulo central.
    assert _el_centro_es_obligatorio(SEMILLAS[1][indice], 14, 25, 9, 16)


@pytest.mark.parametrize("indice", range(len(SEMILLAS[1])))
def test_nivel2_todas_las_celdas_libres_son_alcanzables(indice):
    mapa = SEMILLAS[1][indice]
    inicio = _buscar_celda(mapa, "S")
    libres = {
        (x, y)
        for y, fila in enumerate(mapa)
        for x, celda in enumerate(fila)
        if celda != "1"
    }
    assert _alcanzables(mapa, inicio) == libres


@pytest.mark.parametrize("indice", range(len(SEMILLAS[1])))
def test_nivel2_solo_el_pilar_conocido_es_bloque_2x2_de_muro(indice):
    mapa = SEMILLAS[1][indice]
    bloques = []
    for y in range(len(mapa) - 1):
        for x in range(len(mapa[0]) - 1):
            celdas = (
                mapa[y][x],
                mapa[y][x + 1],
                mapa[y + 1][x],
                mapa[y + 1][x + 1],
            )
            if all(celda == "1" for celda in celdas):
                bloques.append((x, y))
    assert bloques == [(36, 22)]


def test_nivel2_tiene_doce_frutas_y_cinco_monstruos():
    assert len(FRUTAS_POR_NIVEL[1]) == 12
    assert len(MONSTRUOS_POR_NIVEL[1]) == 5


def test_monstruos_nivel2_persiguen_a_cuatro_bloques():
    assert RANGO_DETECCION_NIVEL_2 == 4 * TILE_SIZE
    for datos in MONSTRUOS_POR_NIVEL[1]:
        assert datos["rango_deteccion"] == RANGO_DETECCION_NIVEL_2
        assert datos["velocidad"] < VELOCIDAD_JUGADOR


def test_velocidad_nivel2_es_diez_por_ciento_mayor():
    assert VELOCIDAD_MONSTRUO_NIVEL_2 == int(VELOCIDAD_MONSTRUO_NIVEL_1 * 1.10)
    for datos in MONSTRUOS_POR_NIVEL[1]:
        assert datos["velocidad"] == VELOCIDAD_MONSTRUO_NIVEL_2


def test_tiempo_extra_se_suma_al_nivel2(monkeypatch):
    monkeypatch.setattr(Maze, "_cargar_texturas", lambda self: None)
    pantalla = GameScreen()
    pantalla.maze = Maze(1)
    pantalla._configurar_salida(1, 12)
    assert pantalla.tiempo_base == 75
    assert pantalla.tiempo_extra == 12
    assert pantalla.tiempo_nivel == 87


def test_pausa_tras_dano_detiene_la_persecucion(monkeypatch):
    monkeypatch.setattr(Monster, "_load_sprites", classmethod(lambda cls: None))
    monkeypatch.setattr(Monster, "_escalar_frames", lambda self: None)
    monstruo = Monster(
        0, 0, 51, 51, [], VELOCIDAD_MONSTRUO_NIVEL_2, RANGO_DETECCION_NIVEL_2
    )
    monstruo.persiguiendo = True
    monstruo.camino = [(0, 0)]
    monstruo.pausar_tras_dano()
    assert monstruo.tiempo_espera == PAUSA_MONSTRUO_TRAS_DANO
    assert not monstruo.persiguiendo
    assert monstruo.camino is None


def test_camino_del_monstruo_evita_paredes(monkeypatch):
    monkeypatch.setattr(Monster, "_load_sprites", classmethod(lambda cls: None))
    monkeypatch.setattr(Monster, "_escalar_frames", lambda self: None)

    class MazeFalso:
        tile_size = 10
        mapa = (
            "11111",
            "1S001",
            "10101",
            "10001",
            "11111",
        )

    monstruo = Monster(10, 10, 5, 5, [], 100, 0)
    jugador = pygame.Rect(30, 30, 5, 5)
    camino = monstruo._calcular_camino(MazeFalso(), jugador)

    assert camino
    assert abs(camino[0][0] - 1) + abs(camino[0][1] - 1) == 1
    assert camino[-1] == (3, 3)
    for (x1, y1), (x2, y2) in pairwise(camino):
        assert abs(x1 - x2) + abs(y1 - y2) == 1
        assert MazeFalso.mapa[y2][x2] != "1"


def test_monstruo_recorre_el_nivel2_sin_tocar_paredes(monkeypatch):
    monkeypatch.setattr(Monster, "_load_sprites", classmethod(lambda cls: None))
    monkeypatch.setattr(Monster, "_escalar_frames", lambda self: None)

    class MazeFalso:
        tile_size = TILE_SIZE
        colisiona = Maze.colisiona

        def __init__(self, mapa):
            self.mapa = mapa

    mapa = SEMILLAS[1][0]
    maze = MazeFalso(mapa)
    monstruo = Monster(0, 0, 51, 51, [], VELOCIDAD_MONSTRUO_NIVEL_2)
    monstruo.rect.center = (
        TILE_SIZE + TILE_SIZE // 2,
        TILE_SIZE + TILE_SIZE // 2,
    )
    jugador = pygame.Rect(0, 0, 51, 51)
    jugador.center = (
        (len(mapa[0]) - 2) * TILE_SIZE + TILE_SIZE // 2,
        (len(mapa) - 1) * TILE_SIZE + TILE_SIZE // 2,
    )
    mundo = pygame.Rect(
        0, 0, len(mapa[0]) * TILE_SIZE, len(mapa) * TILE_SIZE
    )
    monstruo.persiguiendo = True

    alcanzado = False
    for _ in range(60 * 60):
        monstruo._perseguir(1 / 60, jugador, maze, mundo)
        assert not maze.colisiona(monstruo.rect)
        if monstruo.rect.colliderect(jugador):
            alcanzado = True
            break
    assert alcanzado
