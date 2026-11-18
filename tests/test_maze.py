"""Tests de las colisiones del laberinto."""

import pygame

from src.world.maze import Maze
from tests.utils import buscar_celda


def _crear_maze(monkeypatch):
    monkeypatch.setattr(Maze, "_cargar_texturas", lambda self: None)
    return Maze(0)


def test_colisiona_con_pared(monkeypatch):
    maze = _crear_maze(monkeypatch)
    assert maze.colisiona(pygame.Rect(0, 0, 10, 10))


def test_posicion_libre_no_colisiona(monkeypatch):
    maze = _crear_maze(monkeypatch)
    x, y = maze.obtener_posiciones_libres()[0]
    assert not maze.colisiona(pygame.Rect(x - 5, y - 5, 10, 10))


def test_spawn_coincide_con_la_semilla(monkeypatch):
    maze = _crear_maze(monkeypatch)
    x, y = buscar_celda(maze.mapa, "S")
    assert maze.spawn.topleft == (x * maze.tile_size, y * maze.tile_size)
    assert not maze.colisiona(maze.spawn)


def test_salida_coincide_con_la_semilla(monkeypatch):
    maze = _crear_maze(monkeypatch)
    x, y = buscar_celda(maze.mapa, "E")
    assert maze.salida.topleft == (x * maze.tile_size, y * maze.tile_size)
    assert not maze.colisiona(maze.salida)
    assert maze.spawn != maze.salida
