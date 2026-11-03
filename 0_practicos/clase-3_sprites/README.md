# Práctico Clase 3 - Sprites, Imágenes y Grupos

Dos mini-juegos con Pygame demostrando Sprites, Groups y colisiones.

## Ejercicio 1
Jugador (nave) moviéndose con flechas, limitado a la ventana, FPS en pantalla.

## Ejercicio 2
Enemigos (aliens) caen desde arriba cada 1s, colisión = Game Over, puntaje por tiempo de supervivencia. **Disparos con ESPACIO** matan enemigos (+10 pts).

## EstructuraS
```
src/
├── main.py      # Game loop principal
├── jugador.py   # Clase Jugador + Disparo
└── enemigo.py   # Clase Enemigo
assets/images/
├── nave.png     # Sprite jugador
└── alien.png    # Sprite enemigo
```

## Ejecutar
Desde la **raíz del proyecto** (`practico-sprite/`):
```bash
python -m src.main
```

Controles: Flechas = mover, Espacio = disparar, Cerrar ventana = salir.