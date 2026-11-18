# 🌿 Maze Level One Game

Videojuego 2D de laberinto desarrollado en Python con Pygame, donde una pequeña personita debe escapar de laberintos ambientados en una selva, recolectando frutas y esquivando monstruos, antes de que se agoten sus vidas o el tiempo disponible.

## Descripción

El jugador controla a un personaje dentro de un laberinto de mayor tamaño que la pantalla, recorrido con ayuda de una cámara que lo sigue en todo momento. El objetivo es alcanzar la salida de cada nivel y, finalmente, completar todos los niveles disponibles para ganar la partida. Durante el recorrido se pueden recolectar frutas de distintos tipos, que suman puntos y pueden otorgar un bonus temporal de inmunidad frente a los monstruos. El puntaje final solo se registra en el ranking cuando el jugador logra la Victoria completando todos los niveles.

El juego tiene **dos niveles**: el primero de 20×13 celdas, pensado como introducción, y el segundo de 40×26 (el doble por lado), con mayor dificultad. El nivel 1 elige al azar entre 3 semillas y el nivel 2 entre 5 semillas propias. El nivel 1 tiene 5 frutas y 1 monstruo; el nivel 2 sube a 12 frutas y 5 monstruos que patrullan y persiguen al jugador cuando se acerca a 4 bloques, además de su propia música de fondo. En ambos niveles las frutas y los monstruos se ubican al azar, sin repetir celdas y lejos del spawn.

## Cómo se juega

- **Movimiento:** `W`, `A`, `S`, `D` o las flechas del teclado.
- **Pantalla completa:** `Alt + Enter` alterna entre modo ventana (1024x768) y pantalla completa.
- **Objetivo:** recolectar frutas y llegar a la salida. Al salir del nivel 1 se pasa directo al nivel 2; la Victoria es recién al completar el nivel 2.
- **Vidas:** el personaje comienza con 5 vidas; se pierde una al ser tocado por un monstruo (salvo inmunidad o invulnerabilidad temporal).
- **Tiempo:** cada nivel tiene un límite en cuenta regresiva (35 s el primero y 75 s el segundo); si se agota, la partida termina en Game Over. Los segundos que sobren del nivel 1 se suman al tiempo inicial del nivel 2, y los que queden al final se usan para el bonus.
- **Fin de partida:** Victoria al completar todos los niveles, o Game Over al perder las 5 vidas o al agotarse el tiempo.

## Nivel 2: más dificultad

El nivel 2 está pensado para que la dificultad no dependa de correr por los bordes, sino de resolver el laberinto:

- **Laberinto más grande:** 40×26 celdas (3080×2002 px), con 5 semillas diseñadas a mano. El borde exterior es de un solo bloque, no hay pasillos 2×2 y la salida `E` se alcanza desde arriba, igual que en el nivel 1.
- **Cruce central obligatorio:** los pasillos perimetrales están segmentados con muros y puertas aisladas. Ninguna ruta puede llegar a la salida usando solo el anillo exterior; hay que atravesar el centro del laberinto.
- **12 frutas:** todas valen 10 puntos. Juntar 3 frutas en 10 segundos activa 5 segundos de inmunidad.
- **5 monstruos con patrulla y persecución:** cada uno recibe un circuito de puntos libres cercano a su spawn y lo recorre con BFS, sin atravesar paredes. Cuando detectan al jugador a 4 bloques (308 px), cambian a persecución, recalculan el camino cada 0,25 s y vuelven a la patrulla al salir del área. Se mueven un 10 % más rápido que los del nivel 1 y se detienen 0,6 s después de golpear.
- **Posiciones aleatorias:** las frutas y los monstruos se eligen entre celdas libres, sin repetir y a una distancia mínima de 4 bloques del spawn. Los monstruos también evitan aparecer cerca de la salida.
- **Tiempo y transición:** el nivel 2 arranca con 75 s base más los segundos sobrantes del nivel 1. El HUD muestra el extra acumulado (por ejemplo, `75 +10` si sobraron 10 s) y la victoria final solo se obtiene al terminarlo.
- **Audio propio:** música `maze_lv2.wav`, además de los efectos de fruta, daño, inmunidad y pasos.

## Funcionalidades

**FASE 1**
- [x] Control del personaje en ocho direcciones.
- [x] Laberinto más grande que la pantalla, con cámara de seguimiento.

**FASE 2**
- [x] Menú principal con opciones de Jugar y Salir.
- [x] Agregar al menú principal opcion de Instrucciones.
- [x] Agregar al menú principal opcion de Tabla de puntos (ranking con el Top 10).

**FASE 3**
- [x] Al menos 3 semillas de laberinto prediseñadas para elegir al azar.
- [x] Creacion del HUD para puntaje, vidas, tiempo y nivel de laberinto.
- [x] Crear salida del laberinto para finalizar nivel, con pantalla final de victoria/game over.
- [x] Agregar tiempo limite para escapar del laberinto.
- [x] Condición de Victoria únicamente al completar todos los niveles.
- [x] Nivel 2 con 5 semillas de 40×26 y cruce central obligatorio.
- [x] Transición al nivel 2 conservando el tiempo sobrante del nivel 1.

**FASE 4**
- [x] Frutas coleccionables de distintos tipos, todas de 10 puntos.
- [x] Bonus temporal de inmunidad al recolectar frutas.
- [x] 12 frutas en el nivel 2, con bonus por juntar 3 en 10 segundos.

**FASE 5**
- [x] Monstruos con patrullas por celdas y área de persecución desde el segundo nivel.
- [x] Sistema de 5 vidas con período de invulnerabilidad tras cada impacto.
- [x] 5 monstruos en el nivel 2 con patrulla BFS, persecución y rango de detección de 4 bloques.
- [x] Frutas y monstruos en posiciones aleatorias, sin repetir y lejos del spawn.

**FASE 6**
- [x] Bonus de puntos por Victoria (vidas restantes y tiempo sobrante).
- [x] Registro de nombre y puntaje en SQLite, solo en caso de Victoria.

**FASE 7 – Preparación multimedia**
- [x] Cargador de imágenes y sonidos

**FASE 8 – Decorado y HUD**
- [x] Paredes y suelo con imágenes
- [x] Frutas con su imagen propia
- [x] Salida con efecto visual
- [x] Iconos en el HUD (vidas, puntos, tiempo)
- [x] Corregir detalles visuales de menú y pantallas en general

**FASE 9 – Animaciones**
- [x] Personaje camina en 8 direcciones
- [x] Enemigos caminan en 4 direcciones

**FASE 10 – Sonido**
- [x] Música de fondo en partida
- [x] Música de victoria
- [x] Música de game over
- [x] Sonido al caminar
- [x] Sonido al comer fruta
- [x] Sonido al recibir daño
- [x] Sonido al activar inmunidad
- [x] Sonidos en menús (navegar, confirmar)

**ANEXOS**
- [ ] Funcionamiento 100% local, sin conexión a Internet.

## Cómo ejecutar el juego

### Desde el ejecutable (recomendado, sin instalar nada)

- [Descargar `MazeLevelOneGame.exe` (v1.0.0)](https://github.com/faausto/maze-level-one-game/releases/download/v1.0.0/MazeLevelOneGame.exe)
- [Ver todas las versiones](https://github.com/faausto/maze-level-one-game/releases)

Es un único archivo para **Windows 10/11 de 64 bits**: incluye Python, Pygame, imágenes y sonidos. No hace falta clonar el repo, instalar Python ni descomprimir nada; guardalo donde quieras y hacé doble clic.

El ranking se guarda en `%APPDATA%\MazeLevelOneGame\ranking.db` y los errores en `%APPDATA%\MazeLevelOneGame\juego.log`. Al estar fuera de la carpeta temporal del ejecutable, el puntaje se conserva al cerrar y reabrir el juego.

> **Windows 11 con Control Inteligente de Aplicaciones activo:** como el `.exe` no está firmado, Windows puede bloquearlo. Si ves ese aviso, andá a *Configuración → Privacidad y seguridad → Seguridad de Windows → Control de aplicaciones y explorador* y desactivá *Control Inteligente de Aplicaciones*. Si en cambio aparece *Más información*, usá *Ejecutar de todos modos*.

### Desde el código fuente

#### Requisitos

- Python 3.10 o superior.
- Pygame (última versión estable).

#### Instrucciones

```bash
# Clonar el repositorio
git clone https://github.com/faausto/maze-level-one-game.git
cd maze-level-one-game

# Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# Instalar las dependencias
pip install -r requirements.txt

# Ejecutar el juego (desde la raíz del proyecto)
python run.py
```

También funciona con el módulo:

```bash
python -m src.main
```

> `python src/main.py` no funciona porque el proyecto importa `from src...`. Ejecutá siempre desde la raíz con `run.py` o `-m src.main`.

## Cómo correr los tests

Los tests usan `pytest`. Primero instalá las dependencias de desarrollo:

```bash
pip install -r requirements-dev.txt
```

Después ejecutalos desde la raíz del proyecto:

```bash
python -m pytest -v
```

Los tests comprueban, entre otras cosas, que las semillas tengan inicio y salida alcanzable y que el tiempo alcance para recorrer el camino más corto, que las colisiones del laberinto funcionen, que el bonus use el tiempo sobrante, que el ranking guarde bien los puntajes y que el nivel 2 tenga sus 5 semillas, 12 frutas y 5 monstruos con rango de persecución. También verifican que las posiciones de frutas y monstruos sean únicas y estén lejos del spawn en ambos niveles, que las patrullas usen celdas libres, que el HUD muestre `75 +10` desde el inicio, que el anillo perimetral no lleve a la salida, que todas las rutas crucen el centro y que no haya pasillos 2×2. No afectan al juego: solo se ejecutan cuando corrés `pytest`.

## Cómo generar el ejecutable

Solo hace falta en Windows, con Python instalado:

```bash
pip install -r requirements-build.txt
.\build_exe.ps1
```

El resultado queda en `dist/MazeLevelOneGame.exe` (carpeta ignorada por git; el binario se distribuye por GitHub Releases). Toda la configuración está en `MazeLevelOneGame.spec`: un solo archivo, sin consola, sin UPX, con los assets incluidos y el icono generado desde `assets/images/background/menu_background.png`.

## Para desarrolladores

Revisar el estilo y los imports con `ruff`:

```bash
ruff check src tests
```

`ruff` es un analizador estático: revisa el código sin ejecutarlo y avisa de imports sin usar, nombres repetidos o errores de estilo. No es parte del juego ni hace falta para jugar; es una herramienta de desarrollo.

## Estructura del proyecto

```
maze-level-one-game/
├── .gitignore
├── README.md
├── requirements.txt          # Dependencias del juego
├── requirements-dev.txt      # Dependencias de desarrollo (pytest, ruff)
├── requirements-build.txt    # Dependencias para generar el .exe
├── MazeLevelOneGame.spec     # Configuración de PyInstaller
├── build_exe.ps1             # Script de compilación del ejecutable
├── run.py                    # Punto de entrada
├── docs/
│   ├── documentacion.md       # Documentación completa del juego
│   └── diagrama_flujo.md      # Diagrama de flujo de pantallas
├── assets/
│   ├── icon.ico              # Icono del ejecutable
│   ├── images/                # Sprites, fondos, iconos
│   ├── sounds/                # Efectos y música
│   └── fonts/                 # Fuentes de texto
├── src/                       # Código fuente del juego
├── tests/                     # Tests automáticos con pytest
└── database/                  # Base de datos SQLite (se genera al jugar; en el exe va a %APPDATA%)
```

## Tecnologías usadas

- **Python 3**
- **Pygame** — motor gráfico y de eventos.
- **SQLite** — persistencia local del ranking de puntuaciones.

## Documentación

Toda la documentación detallada del juego (requerimientos funcionales y no funcionales, mecánica, pantallas, base de datos y diagrama de flujo) se encuentra en:

- [`docs/documentacion.md`](docs/documentacion.md)
- [`docs/diagrama_flujo.md`](docs/diagrama_flujo.md)

## Créditos de audio

Los sonidos y la música provienen de [Freesound](https://freesound.org/). Cada archivo conserva la licencia con la que fue publicado.

| Archivo | Uso | Autor | Licencia | Fuente |
|---|---|---|---|---|
| `maze_lv1.wav` | Música de fondo en partida ("8 Bit Adventure Theme (intro)") | TheLastOneOnEarth | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Freesound](https://freesound.org/people/TheLastOneOnEarth/sounds/732429/) |
| `maze_lv2.wav` | Música de fondo del nivel 2 ("Electric Guitar Loop 1_150bpm") | CAT-FOX_ALEX | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) | [Freesound](https://freesound.org/people/CAT-FOX_ALEX/sounds/874737/) |
| `menu_sound.wav` | Música del menú ("Arcade Intro #2") | tyops | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Freesound](https://freesound.org/people/tyops/sounds/338361/) |
| `success_level.mp3` | Sonido al superar un nivel ("Electronic Victory Sound") | yokomatsuko | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) | [Freesound](https://freesound.org/people/yokomatsuko/sounds/856038/) |
| `final_victory.mp3` | Música de victoria final ("Triumphant success") | mokasza | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Freesound](https://freesound.org/people/mokasza/sounds/810330/) |
| `game_over.wav` | Sonido de Game Over ("8-bit Game Over Sound/Tune") | EVRetro | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) | [Freesound](https://freesound.org/people/EVRetro/sounds/533034/) |
| `step.ogg` | Sonido al caminar ("Steps-Tile_3a") | nuFF3 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Freesound](https://freesound.org/people/nuFF3/sounds/477357/) |
| `collect.wav` | Sonido al recolectar una fruta ("Grab Item") | qubodup | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) | [Freesound](https://freesound.org/people/qubodup/sounds/841596/) |
| `damage.wav` | Sonido al recibir daño ("Damage-1.wav") | Deathscyp | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) | [Freesound](https://freesound.org/people/Deathscyp/sounds/404109/) |
| `inmune.wav` | Sonido al activar la inmunidad ("Rare Item Found") | Qvantor | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) | [Freesound](https://freesound.org/people/Qvantor/sounds/878617/) |
| `menu_select.wav` | Sonido al navegar el menú ("8-Bit Menu Select") | Qvantor | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) | [Freesound](https://freesound.org/people/Qvantor/sounds/878330/) |
| `menu_confirm.wav` | Sonido al confirmar una opción ("Blip 2") | AceOfSpadesProduc100 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Freesound](https://freesound.org/people/AceOfSpadesProduc100/sounds/341024/) |

> **Sobre las licencias:** los archivos **CC0** no requieren atribución obligatoria, pero se listan igual por transparencia. Los archivos **CC BY 4.0** sí requieren conservar autor, título, enlace a la fuente y licencia.

## Autor

**Fausto Ottino**
