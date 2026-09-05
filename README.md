# 🌿 Maze Level One Game

Videojuego 2D de laberinto desarrollado en Python con Pygame, donde una pequeña personita debe escapar de laberintos ambientados en una selva, recolectando frutas y esquivando monstruos, antes de que se agoten sus vidas o el tiempo disponible.

## Descripción

El jugador controla a un personaje dentro de un laberinto de mayor tamaño que la pantalla, recorrido con ayuda de una cámara que lo sigue en todo momento. El objetivo es alcanzar la salida de cada nivel y, finalmente, completar todos los niveles disponibles para ganar la partida. Durante el recorrido se pueden recolectar frutas de distinto valor, que suman puntos y pueden otorgar un bonus temporal de inmunidad frente a los monstruos. El puntaje final solo se registra en el ranking cuando el jugador logra la Victoria completando todos los niveles.

## Cómo se juega

- **Movimiento:** `W`, `A`, `S`, `D` o las flechas del teclado.
- **Objetivo:** recolectar frutas y llegar a la salida de cada nivel, hasta completar el último.
- **Vidas:** el personaje comienza con 5 vidas; se pierde una al ser tocado por un monstruo (salvo inmunidad o invulnerabilidad temporal).
- **Tiempo:** cada nivel tiene un límite de tiempo en cuenta regresiva; si se agota, la partida termina en Game Over.
- **Fin de partida:** Victoria al completar todos los niveles, o Game Over al perder las 5 vidas o al agotarse el tiempo.

## Funcionalidades

**FASE 1**
- [ ] Control del personaje en las cuatro direcciones.
- [ ] Laberinto más grande que la pantalla, con cámara de seguimiento.

**FASE 2**
- [ ] Menú principal con opciones de Jugar y Salir.
- [ ] Agregar al menú principal opcion de Instrucciones.
- [ ] Agregar al menú principal opcion de Tabla de puntos (ranking con el Top 10).

**FASE 3**
- [ ] Al menos 3 semillas de laberinto prediseñadas para elegir al azar.
- [ ] Creacion del HUD para puntaje, vidas, tiempo y nivel de laberinto.
- [ ] Crear salida del laberinto para finalizar nivel, con pantalla final de victoria/game over.
- [ ] Agregar tiempo limite para escapar del laberinto.
- [ ] Condición de Victoria únicamente al completar todos los niveles.

**FASE 4**
- [ ] Frutas coleccionables de distintos tipos, con distinto puntaje cada una.
- [ ] Bonus temporal de inmunidad al recolectar frutas.

**FASE 5**
- [ ] Monstruos con patrones de movimiento predefinidos (y área de persecución desde el segundo nivel).
- [ ] Sistema de 5 vidas con período de invulnerabilidad tras cada impacto.

**FASE 6**
- [ ] Bonus de puntos por Victoria (vidas restantes y tiempo sobrante).
- [ ] Registro de nombre y puntaje en SQLite, solo en caso de Victoria.

**ANEXOS**
- [ ] Funcionamiento 100% local, sin conexión a Internet.

## Cómo ejecutar el juego

### Requisitos

- Python 3.10 o superior.
- Pygame (última versión estable).

### Instrucciones

```bash
# Clonar el repositorio
git clone https://github.com/faausto/maze-level-one-game.git
cd maze-level-one-game

# Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# Instalar las dependencias
pip install -r requirements.txt

# Ejecutar el juego
opcion 1:
python run.py
 
opcion 2: 
python src/main.py 


```

## Estructura del proyecto

```
maze-level-one-game/
├── .gitignore
├── README.md
├── docs/
│   ├── documentacion.md       # Documentación completa del juego
│   └── diagrama_flujo.md      # Diagrama de flujo de pantallas
├── assets/
│   ├── images/                # Sprites, fondos, iconos
│   ├── sounds/                # Efectos y música
│   └── fonts/                 # Fuentes de texto
├── src/                       # Código fuente del juego
└── database/                  # Base de datos SQLite (se genera al jugar)
```

## Tecnologías usadas

- **Python 3**
- **Pygame** — motor gráfico y de eventos.
- **SQLite** — persistencia local del ranking de puntuaciones.

## Documentación

Toda la documentación detallada del juego (requerimientos funcionales y no funcionales, mecánica, pantallas, base de datos y diagrama de flujo) se encuentra en:

- [`docs/documentacion.md`](docs/documentacion.md)
- [`docs/diagrama_flujo.md`](docs/diagrama_flujo.md)

## Autor

**Fausto Ottino**
