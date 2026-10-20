# Práctico Clase 6 - SQLite en Pygame

Laberinto con Pygame que integra una base de datos SQLite para guardar y mostrar un ranking de puntajes.

## Ejercicio 1 — Guardar y leer puntajes
Programa de consola (`ejercicio1.py`) que crea `ranking.db` con la tabla `puntajes`, guarda 3 puntajes de ejemplo y muestra el top 3 ordenado de mayor a menor.

## Ejercicio 2 — Módulo db.py para el ranking
Módulo `db.py` con `init_db()`, `guardar_puntaje(nombre, puntaje)`, `obtener_top(cantidad)` y `borrar_ranking()`. Al ganar, el juego pide el nombre del jugador, guarda el puntaje y muestra el top 5.

## Estructura
```text
main.py       # Game loop, movimiento, colisiones, timer, monedas, meta, ranking
camara.py     # Clase Camara y cálculo del offset
laberinto.py  # Mapa, construcción y dibujo de paredes
audio.py      # Inicialización mixer, carga y reproducción de sonidos/música
hud.py        # Fuente y dibujo del HUD (puntaje, vidas, tiempo)
db.py         # Funciones de base de datos SQLite (init_db, guardar, top, borrar)
ejercicio1.py # Ejercicio de consola: guardar y leer puntajes
ranking.db     # Base de datos generada al ejecutar
assets/sounds/
    soundtrack.wav   # Música de fondo en bucle
    victory.mp3      # Sonido al ganar
```