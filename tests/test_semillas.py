"""Tests de las semillas del laberinto."""

import pytest

from src.world.seeds import SEMILLAS
from tests.utils import buscar_celda, salida_alcanzable


@pytest.mark.parametrize("nivel", range(len(SEMILLAS)))
def test_todas_las_semillas_tienen_salida_alcanzable(nivel):
    for mapa in SEMILLAS[nivel]:
        assert salida_alcanzable(mapa)


def test_todas_las_filas_tienen_el_mismo_largo():
    for nivel in SEMILLAS:
        for mapa in nivel:
            assert len({len(fila) for fila in mapa}) == 1


@pytest.mark.parametrize("nivel", range(len(SEMILLAS)))
def test_cada_semilla_tiene_un_spawn_y_una_salida(nivel):
    for mapa in SEMILLAS[nivel]:
        assert sum(fila.count("S") for fila in mapa) == 1
        assert sum(fila.count("E") for fila in mapa) == 1


@pytest.mark.parametrize("nivel", range(len(SEMILLAS)))
def test_spawn_y_salida_estan_separados(nivel):
    for mapa in SEMILLAS[nivel]:
        spawn_x, spawn_y = buscar_celda(mapa, "S")
        salida_x, salida_y = buscar_celda(mapa, "E")
        assert abs(salida_x - spawn_x) + abs(salida_y - spawn_y) >= 10
