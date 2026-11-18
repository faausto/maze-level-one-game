"""Tests de posiciones aleatorias, patrullas y winnability."""

import math
import random
from collections import deque

import pygame
import pytest

from src.constants import (
    DISTANCIA_MINIMA_SPAWN,
    TILE_SIZE,
    VELOCIDAD_JUGADOR,
)
from src.entities.monster import Monster
from src.screens.game_screen import GameScreen
from src.world.maze import Maze
from src.world.placement import elegir_posiciones
from src.world.seeds import (
    FRUTAS_POR_NIVEL,
    MONSTRUOS_POR_NIVEL,
    NIVELES,
    SEMILLAS,
)
from tests.utils import buscar_celda


def _crear_maze(monkeypatch, nivel):
    monkeypatch.setattr(Maze, "_cargar_texturas", lambda self: None)
    return Maze(nivel)


def _camino_mas_corto(mapa):
    """Devuelve el camino más corto entre S y E, o una lista vacía."""
    inicio = buscar_celda(mapa, "S")
    destino = buscar_celda(mapa, "E")
    cola = deque([inicio])
    previos = {inicio: None}

    while cola:
        actual = cola.popleft()
        if actual == destino:
            break
        x, y = actual
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= ny < len(mapa) and 0 <= nx < len(mapa[0])):
                continue
            if mapa[ny][nx] == "1" or (nx, ny) in previos:
                continue
            previos[(nx, ny)] = actual
            cola.append((nx, ny))

    if destino not in previos:
        return []

    camino = [destino]
    actual = previos[destino]
    while actual is not None and actual != inicio:
        camino.append(actual)
        actual = previos[actual]
    camino.append(inicio)
    camino.reverse()
    return camino


def test_elegir_posiciones_no_repite_y_respeta_distancia():
    disponibles = [(x, y) for x in range(12) for y in range(12)]

    elegidas = elegir_posiciones(
        disponibles,
        6,
        evitar=[(0, 0)],
        distancia_minima=4,
        rng=random.Random(0),
    )

    assert len(elegidas) == 6
    assert len(set(elegidas)) == 6
    assert all(math.dist(posicion, (0, 0)) >= 4 for posicion in elegidas)
    assert all(posicion not in disponibles for posicion in elegidas)


def test_elegir_posiciones_falla_si_faltan_candidatas():
    with pytest.raises(ValueError):
        elegir_posiciones([(0, 0)], 2, distancia_minima=0)


@pytest.mark.parametrize("nivel", range(len(SEMILLAS)))
def test_posiciones_de_frutas_y_monstruos_son_unicas_y_lejos_del_spawn(
    monkeypatch, nivel
):
    maze = _crear_maze(monkeypatch, nivel)
    pantalla = GameScreen()
    pantalla.maze = maze

    frutas, monstruos = pantalla._elegir_posiciones_nivel(nivel)
    todas = frutas + monstruos

    assert len(frutas) == len(FRUTAS_POR_NIVEL[nivel])
    assert len(monstruos) == len(MONSTRUOS_POR_NIVEL[nivel])
    assert len(todas) == len(set(todas))
    assert all(
        math.dist(posicion, maze.spawn.center) >= DISTANCIA_MINIMA_SPAWN
        for posicion in todas
    )
    assert all(
        math.dist(posicion, maze.salida.center) >= DISTANCIA_MINIMA_SPAWN
        for posicion in monstruos
    )


@pytest.mark.parametrize("nivel", range(len(SEMILLAS)))
def test_patrullas_de_monstruos_usan_celdas_libres(monkeypatch, nivel):
    maze = _crear_maze(monkeypatch, nivel)
    monkeypatch.setattr(Monster, "_load_sprites", classmethod(lambda cls: None))
    monkeypatch.setattr(Monster, "_escalar_frames", lambda self: None)

    pantalla = GameScreen()
    pantalla.maze = maze
    _, posiciones_monstruos = pantalla._elegir_posiciones_nivel(nivel)
    monstruos = pantalla._crear_monstruos(nivel, posiciones_monstruos)

    assert len(monstruos) == len(MONSTRUOS_POR_NIVEL[nivel])
    for monstruo in monstruos:
        assert len(monstruo.patrulla) >= 2
        assert monstruo.patrulla[0] == (
            monstruo.rect.centerx // maze.tile_size,
            monstruo.rect.centery // maze.tile_size,
        )
        for x, y in monstruo.patrulla:
            assert 0 <= x < len(maze.mapa[0])
            assert 0 <= y < len(maze.mapa)
            assert maze.mapa[y][x] != "1"


def _maze_falso(mapa, tile_size=20):
    class MazeFalso:
        def __init__(self):
            self.mapa = mapa
            self.tile_size = tile_size

        def colisiona(self, rect):
            return Maze.colisiona(self, rect)

    return MazeFalso()


def test_monstruo_patrulla_entre_celdas_sin_tocar_paredes(monkeypatch):
    monkeypatch.setattr(Monster, "_load_sprites", classmethod(lambda cls: None))
    monkeypatch.setattr(Monster, "_escalar_frames", lambda self: None)

    maze = _maze_falso(
        (
            "1111111",
            "1S00001",
            "1010101",
            "1000001",
            "1111111",
        )
    )
    mundo = pygame.Rect(0, 0, 7 * maze.tile_size, 5 * maze.tile_size)
    monstruo = Monster(
        28,
        28,
        5,
        5,
        [(1, 1), (5, 1), (5, 3), (1, 3)],
        100,
        0,
    )
    jugador_lejano = pygame.Rect(120, 60, 5, 5)

    visitados = set()
    for _ in range(60 * 20):
        monstruo.update(1 / 60, jugador_lejano, maze, mundo)
        assert not maze.colisiona(monstruo.rect)
        visitados.add(monstruo.indice_punto)

    assert len(visitados) > 1


def test_monstruo_vuelve_a_patrullar_al_salir_del_rango(monkeypatch):
    monkeypatch.setattr(Monster, "_load_sprites", classmethod(lambda cls: None))
    monkeypatch.setattr(Monster, "_escalar_frames", lambda self: None)

    maze = _maze_falso(
        (
            "1111111",
            "1S00001",
            "1010101",
            "1000001",
            "1111111",
        )
    )
    mundo = pygame.Rect(0, 0, 7 * maze.tile_size, 5 * maze.tile_size)
    monstruo = Monster(
        28,
        28,
        5,
        5,
        [(1, 1), (5, 1)],
        100,
        60,
    )
    jugador_cerca = pygame.Rect(0, 0, 5, 5)
    jugador_cerca.center = (30, 30)
    jugador_lejos = pygame.Rect(0, 0, 5, 5)
    jugador_lejos.center = (120, 30)

    monstruo.update(1 / 60, jugador_cerca, maze, mundo)
    assert monstruo.persiguiendo

    monstruo.update(1 / 60, jugador_lejos, maze, mundo)
    assert not monstruo.persiguiendo


@pytest.mark.parametrize("nivel", range(len(SEMILLAS)))
def test_tiempo_alcanza_para_el_camino_mas_corto(nivel):
    for mapa in SEMILLAS[nivel]:
        camino = _camino_mas_corto(mapa)
        assert camino

        tiempo_minimo = (len(camino) - 1) * TILE_SIZE / VELOCIDAD_JUGADOR
        # Se exige la mitad del tiempo disponible para dejar margen
        # a esquivar monstruos y recolectar frutas.
        assert tiempo_minimo < NIVELES[nivel]["tiempo"] / 2
