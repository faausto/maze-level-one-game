"""Selección de posiciones y patrullas para las entidades del laberinto."""

import math
import random
from collections import deque


def elegir_posiciones(
    disponibles, cantidad, evitar=(), distancia_minima=0.0, rng=None
):
    """Elige posiciones al azar, sin repetir y lejos de los puntos de `evitar`.

    Las posiciones elegidas se quitan de `disponibles` para que dos sistemas
    (por ejemplo, frutas y monstruos) no compartan la misma celda.
    """
    if cantidad < 0:
        raise ValueError("La cantidad de posiciones no puede ser negativa")

    generador = rng or random
    candidatas = [
        posicion
        for posicion in disponibles
        if all(
            math.dist(posicion, punto) >= distancia_minima
            for punto in evitar
        )
    ]
    if len(candidatas) < cantidad:
        raise ValueError(
            "No hay suficientes posiciones libres: "
            f"se pidieron {cantidad} y hay {len(candidatas)}"
        )

    elegidas = generador.sample(candidatas, cantidad)
    for posicion in elegidas:
        disponibles.remove(posicion)
    return elegidas


def generar_patrulla(maze, celda_inicio, cantidad=3, radio=6, rng=None):
    """Genera un circuito de puntos libres cercanos a `celda_inicio`.

    La lista devuelta empieza en la celda inicial y continúa con celdas
    normales (no spawn ni salida) a una distancia BFS máxima de `radio`.
    """
    generador = rng or random
    cercanas = _celdas_alcanzables(maze, celda_inicio, radio)
    candidatas = [
        celda
        for celda in cercanas
        if celda != celda_inicio and maze.mapa[celda[1]][celda[0]] == "0"
    ]
    cantidad = min(cantidad, len(candidatas))
    elegidas = generador.sample(candidatas, cantidad) if cantidad else []
    return [celda_inicio, *elegidas]


def _celdas_alcanzables(maze, inicio, radio):
    """Devuelve las celdas libres alcanzables en `radio` pasos o menos."""
    alto, ancho = len(maze.mapa), len(maze.mapa[0])
    distancias = {inicio: 0}
    cola = deque([inicio])

    while cola:
        x, y = cola.popleft()
        distancia = distancias[(x, y)]
        if distancia >= radio:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < ancho and 0 <= ny < alto):
                continue
            if maze.mapa[ny][nx] == "1" or (nx, ny) in distancias:
                continue
            distancias[(nx, ny)] = distancia + 1
            cola.append((nx, ny))

    return list(distancias)
