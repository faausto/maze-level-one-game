# Práctico Clase 5 - Sonido, Timers y HUD

Laberinto con Pygame que integra efectos de sonido, música de fondo, timers con delta time y HUD con puntaje, vidas y tiempo.

## Ejercicio 1 — Sonido y música
Inicialización del mixer, carga de sonidos una sola vez al inicio. Música de fondo (`soundtrack.wav`) en bucle con volumen bajo (0.2). Efecto de victoria (`victory.mp3`) al llegar a la meta, que se reproduce completo antes de cerrar el juego.

## Ejercicio 2 — Timer + HUD
Timer con delta time que genera monedas cada 5 segundos (máximo 10). Movimiento del jugador usando delta time (velocidad en px/s). HUD dibujado al final sin offset de cámara: puntaje arriba a la izquierda, vidas arriba a la derecha, tiempo transcurrido en el centro.

## Estructura
```text
main.py       # Game loop, movimiento, colisiones, timer, monedas, meta
camara.py     # Clase Camara y cálculo del offset
laberinto.py  # Mapa, construcción y dibujo de paredes
audio.py      # Inicialización mixer, carga y reproducción de sonidos/música
hud.py        # Fuente y dibujo del HUD (puntaje, vidas, tiempo)
assets/sounds/
    soundtrack.wav   # Música de fondo en bucle
    victory.mp3      # Sonido al ganar
```