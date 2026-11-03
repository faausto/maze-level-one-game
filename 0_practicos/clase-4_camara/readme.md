# Práctico Clase 4 - Cámara y Scroll

Laberinto con Pygame que demuestra cámara de seguimiento, scroll, colisiones y separación entre coordenadas del mundo y de pantalla.

## Ejercicio 1
Cámara de seguimiento que centra al jugador y limita el desplazamiento a los bordes del mapa.

## Ejercicio 2
Laberinto construido a partir de una grilla de texto (`1` = pared, `0` = camino). Jugador controlado con flechas, colisiones contra paredes, cámara con scroll y meta para completar el recorrido.

## Estructura
```text
main.py       # Game loop, movimiento, colisiones y meta
camara.py     # Clase Camara y cálculo del offset
laberinto.py  # Mapa, construcción y dibujo de paredes