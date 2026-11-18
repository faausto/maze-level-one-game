"""Funciones compartidas por los tests."""

from collections import deque


def buscar_celda(mapa, caracter):
    """Devuelve las coordenadas (x, y) de la primera celda indicada."""
    for y, fila in enumerate(mapa):
        x = fila.find(caracter)
        if x != -1:
            return x, y
    raise ValueError(f"La semilla no tiene la celda '{caracter}'")


def salida_alcanzable(mapa):
    """Indica si se puede llegar desde la celda S hasta la celda E."""
    inicio = buscar_celda(mapa, "S")
    destino = buscar_celda(mapa, "E")
    pendientes = deque([inicio])
    visitadas = {inicio}
    alto = len(mapa)
    ancho = len(mapa[0])

    while pendientes:
        x, y = pendientes.popleft()
        if (x, y) == destino:
            return True

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < ancho and 0 <= ny < alto):
                continue
            if mapa[ny][nx] == "1":
                continue
            if (nx, ny) in visitadas:
                continue
            visitadas.add((nx, ny))
            pendientes.append((nx, ny))

    return False
