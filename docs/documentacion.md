# Documentación del juego — Maze Level One Game

## 1. Descripción general del juego

**Maze Level One Game** es un videojuego 2D de laberinto desarrollado en Python con Pygame, donde el jugador controla a una pequeña personita que debe escapar de laberintos ambientados en una selva. El objetivo es recorrer el laberinto, recolectar frutas de distinto valor para sumar puntos y alcanzar la salida de todos los niveles disponibles antes de perder las 5 unidades de vida o de que se agote el tiempo límite de cada nivel. El personaje se controla con las teclas `W`, `A`, `S`, `D` o las teclas de dirección. La partida termina en **Victoria** cuando el jugador alcanza la salida del último nivel, o en **Game Over** si pierde todas sus vidas o se le acaba el tiempo en cualquier nivel; solo al completar todos los niveles con éxito se registra el puntaje en el ranking.

---

## 2.1. Requerimientos Funcionales (RF)

- **RF-01:** El sistema deberá mostrar un menú principal con las opciones Jugar, Instrucciones, Tabla de puntos y Salir.
- **RF-02:** Al seleccionar "Jugar", el sistema deberá iniciar una nueva partida comenzando por el primer nivel, con el personaje en su posición inicial, 5 vidas, 0 puntos y el tiempo en su valor máximo.
- **RF-03:** El sistema deberá permitir controlar el movimiento del personaje mediante las teclas `W`, `A`, `S`, `D` o las teclas de dirección, en las cuatro direcciones principales.
- **RF-04:** El personaje no deberá poder atravesar las paredes ni los límites físicos del laberinto.
- **RF-05:** Cada nivel deberá tener dimensiones superiores al área visible de la ventana, y la cámara deberá seguir al personaje mostrando únicamente la zona del laberinto a su alrededor.
- **RF-06:** El proyecto deberá contar con al menos 2 niveles jugables, desarrollados de forma incremental. Cada nivel deberá tener 3 semillas de laberinto prediseñadas, eligiéndose una al azar al iniciar o avanzar de nivel.
- **RF-07:** El sistema deberá distribuir frutas coleccionables de al menos 3 tipos distintos en posiciones predeterminadas de cada laberinto, cada una otorgando una cantidad de puntos diferente (mínimo 10 puntos). Las frutas de mayor valor podrán ubicarse en zonas alejadas del camino principal a la salida.
- **RF-08:** Al recolectar cierta cantidad de frutas del mismo tipo, o cierta cantidad de frutas dentro de un intervalo de tiempo, el sistema deberá otorgar un bonus temporal de inmunidad, durante el cual el contacto con monstruos no restará vidas.
- **RF-09:** Cada nivel deberá contener monstruos que se desplacen mediante patrones de movimiento predefinidos. A partir del segundo nivel, los monstruos podrán contar con un área de detección que, al ser invadida por el personaje, activará una persecución temporal.
- **RF-10:** El sistema deberá detectar el contacto entre el personaje y los monstruos, restando una unidad de vida salvo que el personaje esté bajo el bonus de inmunidad o en período de invulnerabilidad posterior a un impacto.
- **RF-11:** El personaje deberá comenzar cada partida con 5 unidades de vida, mostradas visualmente en el HUD mediante cinco indicadores.
- **RF-12:** Cada nivel deberá contar con un tiempo límite en cuenta regresiva, visible en el HUD; si llega a cero antes de alcanzar la salida, la partida finaliza en Game Over.
- **RF-13:** Cuando el personaje pierda todas sus vidas o se agote el tiempo, la partida deberá finalizar con resultado Game Over y el puntaje obtenido no se registrará.
- **RF-14:** Cuando el personaje alcance la salida de un nivel que no sea el último, el sistema deberá avanzar automáticamente al siguiente nivel, conservando vidas y puntaje, y reiniciando el tiempo y la selección de semilla.
- **RF-15:** El jugador deberá ganar la partida únicamente al alcanzar la salida del último nivel, mostrando el resultado Victoria. Completar solo un nivel intermedio no constituye victoria.
- **RF-16:** Al completar la partida con Victoria, el sistema deberá sumar un bonus de 100 puntos, más 50 puntos por cada vida restante y 5 puntos por cada segundo sobrante del último nivel.
- **RF-17:** Al finalizar la partida con Victoria, el sistema deberá solicitar el nombre del jugador y registrar el nombre y el puntaje final en la base de datos SQLite. No se podrá registrar puntaje si el resultado fue Game Over.
- **RF-18:** El sistema deberá permitir consultar una tabla de puntos (ranking) con las 10 mejores puntuaciones registradas, mostrando posición, nombre y puntos.
- **RF-19:** Desde la pantalla final, el jugador podrá elegir jugar de nuevo (reiniciando desde el primer nivel con nuevas semillas al azar) o volver al menú principal.
- **RF-20:** Al seleccionar "Salir" desde el menú principal, el sistema deberá cerrar correctamente la aplicación.

---

## 2.2. Requerimientos No Funcionales (RNF)

- **RNF-01:** El juego deberá desarrollarse en Python utilizando la biblioteca Pygame.
- **RNF-02:** El juego deberá funcionar completamente de manera local, sin requerir conexión a Internet en ningún momento.
- **RNF-03:** La persistencia de puntuaciones deberá realizarse mediante una base de datos SQLite almacenada localmente.
- **RNF-04:** El juego deberá mantener una ejecución fluida (apuntando a 60 FPS), sin interrupciones perceptibles durante el movimiento del personaje, la cámara y los monstruos.
- **RNF-05:** Las acciones del jugador, colisiones, recolección de frutas y activación del bonus de inmunidad deberán procesarse sin demoras perceptibles.
- **RNF-06:** El código deberá organizarse de forma modular, separando pantallas, jugador, niveles/laberintos, semillas, frutas, monstruos, puntuación y base de datos.
- **RNF-07:** La versión final deberá poder ejecutarse en Windows mediante un archivo `.exe`, sin requerir que el usuario ejecute directamente el código fuente.
- **RNF-08:** La estructura del proyecto deberá permitir incorporar nuevos niveles y semillas en el futuro sin modificar completamente la arquitectura del juego.
- **RNF-09:** La interfaz deberá mantener una estética visual consistente (pixel art estilo selva) a lo largo de todas las pantallas.
- **RNF-10:** El sistema deberá cerrar correctamente los recursos utilizados, incluyendo la conexión a la base de datos, al salir del juego.

---

## 3. Detalle de la mecánica del juego

**¿Qué controla el jugador y con qué teclas?**
El jugador controla a una personita dentro del laberinto, desplazándose en las cuatro direcciones con las teclas `W`, `A`, `S`, `D` o las flechas del teclado.

**¿Cómo se suman puntos?**
Se suman puntos al recolectar frutas (mínimo 10 puntos cada una, según su tipo), y al completar la partida con Victoria se suman bonus adicionales: 100 puntos fijos, 50 puntos por cada vida restante y 5 puntos por cada segundo sobrante de tiempo en el último nivel.

**¿Hay vidas? ¿Cuántas? ¿Cómo se pierden?**
Sí, el personaje comienza cada partida con 5 vidas. Se pierde una vida al ser tocado por un monstruo, salvo que el personaje esté bajo el bonus de inmunidad o dentro de su breve período de invulnerabilidad posterior a un impacto (para evitar perder varias vidas por un mismo contacto).

**¿La dificultad aumenta con el tiempo?**
La dificultad no escala dentro de un mismo nivel mediante velocidad creciente, sino a través de la progresión entre niveles: el segundo nivel incorpora monstruos con área de detección y persecución temporal, además de un laberinto más complejo. El tiempo límite en cuenta regresiva también presiona al jugador a no explorar indefinidamente.

**¿Qué elementos aparecen en pantalla?**
El personaje jugable, las paredes y el piso del laberinto, monstruos con patrones de movimiento (y área de persecución desde el nivel 2), frutas coleccionables de distintos tipos, la salida del nivel, y un HUD con vidas, puntaje y tiempo restante.

**¿Qué hace que el juego termine?**
El juego termina en **Victoria** cuando el personaje alcanza la salida del último nivel disponible, o en **Game Over** cuando el personaje pierde sus 5 vidas o se agota el tiempo límite en cualquier nivel.

---

## 4. Pantallas a crear

Estética general del juego: **pixel art estilo selva/jungla**, cálido y colorido, con tipografía retro tipo *Press Start 2P* (o similar) en color crema sobre paneles de madera oscura.

| Pantalla | Qué muestra | Qué se puede hacer |
|---|---|---|
| Inicio (Menú principal) | Título "Maze Level One Game", opciones Jugar / Instrucciones / Tabla de puntos / Salir | Navegar el menú y seleccionar una opción |
| Instrucciones | Explicación breve de controles, objetivo, vidas, tiempo y frutas | Volver al menú principal |
| Juego | El laberinto con el personaje, monstruos, frutas y salida, más el HUD (vidas, puntaje, tiempo, nivel actual) | Moverse por el laberinto, recolectar frutas, esquivar monstruos |
| Resultado (Victoria / Game Over) | Resultado de la partida y puntaje final obtenido | Ver el resultado antes de continuar |
| Ranking / Tabla de puntos | Listado de las 10 mejores puntuaciones (posición, nombre, puntos) | Consultar los mejores puntajes |
| Final | Resultado de la partida y, en caso de Victoria, el ranking actualizado | Elegir "Jugar de nuevo" o "Volver al menú principal" |

---

## 5. Estructura de la base de datos (SQLite)

**Tabla `ranking`:**

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Identificador único de cada registro |
| nombre | TEXT | Nombre o iniciales del jugador |
| puntaje | INTEGER | Puntaje final obtenido en la partida |
| fecha | TEXT | Fecha en que se jugó la partida |

**Sentencia SQL de creación:**

```sql
CREATE TABLE IF NOT EXISTS ranking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    puntaje INTEGER NOT NULL,
    fecha TEXT NOT NULL
);
```

**¿Cuándo se guarda un registro?**
Únicamente al finalizar la partida con resultado **Victoria**, es decir, cuando el jugador completa todos los niveles disponibles alcanzando la salida del último de ellos. Si el resultado es Game Over, no se guarda ningún registro.

**¿Cómo se obtiene el Top 10?**
Se consultan los registros de la tabla `ranking` ordenados por el campo `puntaje` de forma descendente, tomando únicamente los primeros 10 resultados.

---

## 6. Diagrama de flujo incial de pantallas

El diagrama detallado se encuentra en `docs/diagrama_flujo.md`. El flujo general de pantallas es el siguiente:

```
Inicio (Menú principal)
   │
   ├── Instrucciones ──► (volver a Inicio)
   ├── Tabla de puntos (Ranking) ──► (volver a Inicio)
   └── Jugar
          │
          ▼
       Juego (Nivel actual)
          │
          ├── Alcanza salida de nivel intermedio ──► avanza al siguiente nivel (vuelve a "Juego")
          ├── Alcanza salida del último nivel ──► Resultado: Victoria ──► Ingreso de nombre ──► Registro en SQLite ──► Pantalla Final ──► Jugar de nuevo / Volver al menú
          └── Pierde 5 vidas o se agota el tiempo ──► Resultado: Game Over ──► Pantalla Final ──► Jugar de nuevo / Volver al menú
```
