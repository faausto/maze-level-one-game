# Requerimientos del sistema — Juego 2D de laberinto

## 1. Descripción general

El proyecto consiste en un videojuego 2D desarrollado en Python utilizando la biblioteca Pygame. El jugador deberá controlar un personaje (una personita) dentro de un laberinto de dimensiones considerablemente mayores que el área visible de la pantalla.

El objetivo principal será encontrar y alcanzar la salida de cada laberinto y, finalmente, completar la totalidad de los niveles del juego antes de perder las 5 unidades de vida o de que se agote el tiempo disponible. Durante el recorrido, el jugador podrá recolectar frutas de distintos tipos para aumentar su puntuación, y deberá evitar monstruos que patrullan el laberinto.

El primer alcance del proyecto contempla al menos 2 niveles jugables, desarrollados de forma incremental (primero un nivel funcional, luego el segundo), cada uno con 3 semillas de laberinto prediseñadas entre las cuales el sistema elegirá una al azar al iniciar la partida. El sistema se desarrollará para funcionar completamente de manera local y sin conexión a Internet. Las puntuaciones se almacenarán mediante una base de datos SQLite, y únicamente se registrarán cuando el jugador complete el juego en su totalidad (es decir, alcance la salida de todos los niveles disponibles).

Al finalizar el desarrollo, el juego deberá poder distribuirse como un archivo ejecutable `.exe`.

---

# 2. Requerimientos funcionales

## RF-01 — Menú principal

El sistema deberá mostrar un menú principal al iniciar el juego.

El menú deberá contener las siguientes opciones:

- Jugar.
- Instrucciones del juego.
- Tabla de puntos.
- Salir.

## RF-02 — Inicio de una partida

Al seleccionar la opción "Jugar", el sistema deberá iniciar una nueva partida comenzando por el primer nivel disponible.

La partida comenzará con el personaje ubicado en la posición inicial predefinida del laberinto correspondiente, con 5 vidas, 0 puntos y el contador de tiempo en su valor máximo.

## RF-03 — Control del personaje

El sistema deberá permitir controlar el movimiento del personaje mediante:

- Teclas `W`, `A`, `S` y `D`.
- Teclas de dirección del teclado.

El personaje deberá desplazarse en las cuatro direcciones principales.

## RF-04 — Restricción del movimiento por el laberinto

El personaje no deberá poder atravesar las paredes ni los límites físicos del laberinto.

El movimiento deberá respetar la estructura del mapa.

## RF-05 — Laberinto de mayor tamaño que la pantalla

Cada nivel deberá tener dimensiones superiores al área visible de la ventana del juego.

El jugador deberá poder recorrer diferentes zonas del laberinto sin visualizar simultáneamente todo el mapa.

## RF-06 — Cámara de seguimiento

El sistema deberá implementar una cámara que siga el desplazamiento del personaje.

A medida que el jugador avance, la cámara deberá mostrar las diferentes zonas del laberinto correspondientes a su posición.

Las zonas que queden fuera del área visible dejarán de mostrarse en pantalla, aunque continuarán formando parte del mapa.

## RF-07 — Niveles y semillas prediseñadas

El primer alcance del proyecto deberá contar con al menos 2 niveles jugables. El desarrollo se realizará de forma incremental: primero se implementará y validará un único nivel funcional, y luego se incorporará el segundo. Si el tiempo de desarrollo lo permite, podrán agregarse niveles adicionales sin modificar la arquitectura general del juego.

Cada nivel deberá contar con al menos 3 semillas de laberinto diseñadas previamente: el nivel 1 usa 3 y el nivel 2 usa 5. Al iniciar (o reiniciar) una partida, el sistema deberá seleccionar aleatoriamente una de las semillas correspondientes a cada nivel.

El trazado de paredes y la posición de la salida de cada semilla no deberán generarse de forma procedural; las posiciones de frutas y monstruos se sortean entre celdas libres, sin repetir y lejos del spawn. La elección de qué semilla se utiliza en cada partida también será aleatoria.

## RF-08 — Objetos coleccionables (frutas)

El sistema deberá distribuir objetos de tipo fruta en posiciones aleatorias entre las celdas libres de cada laberinto, sin repetir celdas y a una distancia mínima del spawn.

El jugador podrá recoger una fruta al entrar en contacto con ella.

Deberá existir más de un tipo de fruta. Todas otorgan la misma recompensa de 10 puntos; la variedad es visual. El incentivo para recolectarlas es el bonus de inmunidad por cantidad en un intervalo de tiempo.

Las frutas podrán quedar en zonas alejadas o secundarias del laberinto, no necesariamente sobre el camino requerido para llegar a la salida, de modo que el jugador deba desviarse voluntariamente del recorrido principal para recolectarlas.

## RF-09 — Puntuación por frutas

Cada fruta recogida deberá otorgar **10 puntos** al jugador.

Habrá al menos 3 tipos de frutas distintos, todos con el mismo valor de 10 puntos, distribuidos en el mapa.

Una fruta recogida deberá dejar de estar disponible durante el resto de la partida.

Las frutas no recogidas deberán permanecer disponibles durante toda la partida y no deberán reaparecer en nuevas posiciones.

## RF-10 — Bonus de inmunidad por recolección

El sistema deberá otorgar un bonus temporal de inmunidad al jugador cuando este recolecte una determinada cantidad de frutas dentro de un intervalo de tiempo definido.

Durante el período de inmunidad, el contacto con monstruos no deberá restar unidades de vida al personaje.

La cantidad de frutas necesaria, la ventana de tiempo considerada y la duración de la inmunidad quedan sujetas a ajuste durante el desarrollo y balanceo del juego.

## RF-11 — Monstruos

Cada nivel deberá contener monstruos que representen un peligro para el jugador.

Los monstruos deberán patrullar entre puntos libres cercanos a su posición inicial, elegidos al azar, recorriéndolos con pathfinding para no atravesar paredes y regresando al punto de partida del circuito.

En el primer nivel no se requerirá persecución dinámica ni detección del jugador por parte de los monstruos.

A partir del segundo nivel, los monstruos podrán contar además con un área de detección alrededor de su recorrido: si el personaje ingresa a dicha área, el monstruo comenzará a perseguirlo, ya sea durante un tiempo determinado o hasta que el personaje abandone un área mayor de persecución, momento en el cual el monstruo deberá regresar a su patrulla por defecto. Esta persecución seguirá sin ser una inteligencia artificial avanzada.

## RF-12 — Colisión con monstruos

El sistema deberá detectar el contacto entre el personaje y los monstruos.

Cuando el personaje sea alcanzado por un monstruo y no se encuentre bajo el efecto del bonus de inmunidad (RF-10), deberá perder una unidad de vida.

## RF-13 — Sistema de vidas

El personaje deberá comenzar cada partida con **5 unidades de vida**, las cuales se mantendrán a través de los distintos niveles hasta que la partida finalice.

La interfaz deberá mostrar visualmente las unidades de vida disponibles mediante cinco barras o indicadores.

Cada contacto válido con un monstruo deberá reducir una unidad de vida, salvo que el personaje se encuentre en período de invulnerabilidad o bajo el bonus de inmunidad.

El sistema deberá evitar que un mismo contacto produzca una pérdida ilimitada de vidas mientras el personaje permanece en contacto con el monstruo. Para ello, deberá existir un breve período de invulnerabilidad posterior al impacto.

## RF-14 — Límite de tiempo

Cada nivel deberá contar con un tiempo límite en cuenta regresiva para que el jugador alcance la salida.

El HUD deberá mostrar el tiempo restante de forma clara durante toda la partida.

Si el contador de tiempo llega a cero antes de que el personaje alcance la salida del nivel en curso, la partida deberá finalizar con el resultado **Game Over**.

El valor exacto del tiempo asignado a cada nivel queda sujeto a ajuste durante el desarrollo y balanceo del juego.

## RF-15 — Fin de partida por pérdida

Cuando el personaje pierda todas sus unidades de vida, o se agote el tiempo determinado del nivel en curso, la partida deberá finalizar y el sistema deberá mostrar el resultado **Game Over**.

La puntuación obtenida hasta ese momento se perderá y no se registrará en la base de datos, cualquiera sea el nivel en el que haya ocurrido la pérdida.

## RF-16 — Salida del laberinto y avance de nivel

Cada nivel deberá contener una salida ubicada en una posición predeterminada, la cual permanecerá disponible durante toda la partida.

Cuando el personaje entre en contacto con la salida de un nivel que **no** sea el último, el sistema deberá dar por completado ese nivel y avanzar automáticamente al siguiente, conservando las vidas restantes, la puntuación acumulada y seleccionando aleatoriamente una nueva semilla para el nivel siguiente. El contador de tiempo se reiniciará para el nuevo nivel.

No será necesario presionar ninguna tecla ni realizar una acción adicional para completar un nivel o avanzar al siguiente.

## RF-17 — Condición de victoria final

El jugador deberá ganar la partida únicamente cuando el personaje alcance la salida del **último** nivel disponible, habiendo completado previamente todos los niveles anteriores.

Al cumplirse esta condición, la partida deberá finalizar y el sistema deberá mostrar el resultado **Victoria**.

Completar únicamente el primer nivel (u otro nivel intermedio) no constituye por sí solo una condición de victoria ni habilita el registro de puntaje.

## RF-18 — Bonus por victoria

Al completar exitosamente la partida (es decir, alcanzar la salida del último nivel), el sistema deberá agregar un bonus de **100 puntos** a la puntuación acumulada.

Adicionalmente, sumará **50 puntos** por cada unidad de vida restante al finalizar, y **5 puntos** por cada segundo restante del contador de tiempo del último nivel.

La puntuación final deberá contemplar los puntos obtenidos mediante frutas a lo largo de todos los niveles recorridos, más los bonus de victoria.

## RF-19 — Registro de puntuación

Al finalizar una partida con resultado de **Victoria** (es decir, habiendo completado todos los niveles), el sistema deberá solicitar al jugador que ingrese su nombre.

Una vez ingresado el nombre, el sistema deberá registrar el nombre y la puntuación final obtenida en la base de datos SQLite.

El jugador **no** podrá registrar su puntaje si la partida finalizó en Game Over, ni si únicamente completó uno o más niveles sin llegar a la condición de victoria final.

## RF-20 — Persistencia de puntuaciones

El sistema deberá utilizar una base de datos SQLite almacenada localmente para conservar las puntuaciones.

La información deberá permanecer disponible después de cerrar y volver a iniciar el juego.

No se deberá requerir conexión a Internet para almacenar o consultar las puntuaciones.

La base de datos guardará nombre y puntaje.

## RF-21 — Tabla de puntos

La opción "Tabla de puntos" del menú principal deberá permitir consultar las mejores puntuaciones registradas.

La tabla deberá mostrar únicamente:

- Posición.
- Nombre.
- Puntos.

## RF-22 — Ranking Top 10

La tabla de puntos deberá mostrar como máximo las **10 mejores puntuaciones**.

Las puntuaciones inferiores que se encuentren fuera de las primeras diez posiciones no deberán mostrarse en el ranking.

Cuando se registre una nueva puntuación que se encuentre entre las diez mejores, deberá incorporarse al ranking y desplazar las posiciones inferiores según corresponda.

## RF-23 — Pantalla final de victoria

Luego de finalizar el juego con Victoria (todos los niveles completados), el jugador registra su puntaje con su nombre.

Después de registrar su puntaje, aparecerá la pantalla final con el ranking Top 10 de puntajes y las opciones para que el jugador elija:

- Jugar de nuevo.
- Volver al menú principal.

## RF-24 — Pantalla final de game over

La pantalla final de Game Over solo deberá permitir al jugador elegir entre:

- Jugar de nuevo.
- Volver al menú principal.

No deberá solicitarse el ingreso de nombre ni registrarse puntaje alguno en este caso.

## RF-25 — Jugar de nuevo

Al seleccionar "Jugar de nuevo", el sistema deberá iniciar una nueva partida desde el primer nivel, eligiendo aleatoriamente una de las semillas predeterminadas para cada nivel a medida que se avance.

El jugador deberá comenzar nuevamente con 5 vidas, la puntuación deberá reiniciarse a cero y el contador de tiempo deberá reiniciarse al valor correspondiente al primer nivel.

## RF-26 — Regresar al menú principal

Al seleccionar "Volver al menú principal", el sistema deberá finalizar la partida actual (sin registrar puntaje si no hubo Victoria final) y regresar al menú principal.

## RF-27 — Salida del juego

Al seleccionar "Salir" desde el menú principal, el sistema deberá cerrar correctamente la aplicación.

---

# 3. Requerimientos no funcionales

## RNF-01 — Plataforma de desarrollo

El juego deberá desarrollarse utilizando Python y la biblioteca Pygame.

## RNF-02 — Ejecución local

El juego deberá funcionar completamente de manera local.

No deberá requerir conexión a Internet para iniciar, jugar, guardar puntuaciones, consultar el ranking ni finalizar una partida.

## RNF-03 — Base de datos local

La persistencia de datos deberá realizarse mediante SQLite.

La base de datos deberá estar disponible localmente junto con la aplicación.

## RNF-04 — Rendimiento

El juego deberá mantener una ejecución fluida durante la partida, procurando una tasa de actualización estable y sin interrupciones perceptibles durante el movimiento del personaje, la cámara y los monstruos (incluido su comportamiento de persecución por área a partir del segundo nivel).

## RNF-05 — Tiempo de respuesta

Las acciones del jugador, las colisiones, la recolección de frutas y la activación/finalización del bonus de inmunidad deberán procesarse sin demoras perceptibles.

## RNF-06 — Usabilidad

La interfaz deberá presentar un HUD con información de vidas, tiempo en cuenta regresiva, nivel actual y puntuación de manera clara y comprensible para el jugador.

Las opciones de los menús deberán poder identificarse fácilmente.

## RNF-07 — Compatibilidad de ejecución

La versión final del proyecto deberá poder ejecutarse en Windows mediante un archivo ejecutable `.exe`, sin requerir que el usuario ejecute directamente el código fuente de Python.

## RNF-08 — Portabilidad

El juego deberá poder ejecutarse sin depender de servicios externos, servidores o conexiones remotas.

## RNF-09 — Integridad de los datos

El sistema deberá evitar la pérdida o corrupción de las puntuaciones almacenadas durante el funcionamiento normal de la aplicación.

## RNF-10 — Mantenibilidad

El código deberá organizarse de manera modular, separando las responsabilidades principales del juego, como gestión de pantallas, jugador, niveles/laberintos, semillas, frutas, monstruos, puntuación, base de datos y lógica general de la partida.

## RNF-11 — Escalabilidad

La estructura del proyecto deberá permitir incorporar nuevos niveles y nuevas semillas de laberinto en futuras versiones sin necesidad de modificar completamente la arquitectura del juego.

El primer alcance estará compuesto por al menos 2 niveles, desarrollados de forma incremental.

## RNF-12 — Funcionamiento sin servicios externos

Ninguna funcionalidad del juego deberá depender de APIs, servicios web, servidores externos, cuentas de usuario o almacenamiento en la nube.

## RNF-13 — Consistencia visual

Los elementos de la interfaz deberán mantener una presentación consistente entre la fluidez del juego.

## RNF-14 — Recuperación ante cierre normal

El sistema deberá cerrar correctamente los recursos utilizados por la aplicación, incluyendo la conexión o acceso a la base de datos, al salir del juego.

---

# 4. Alcance inicial

La primera versión del proyecto incluirá:

- Al menos 2 niveles, desarrollados de forma incremental (primero uno funcional, luego el segundo).
- 3 semillas de laberinto prediseñadas por nivel, elegidas al azar al iniciar/avanzar de nivel.
- Un personaje controlable.
- Cámara de seguimiento.
- Tiempo límite en cuenta regresiva por nivel.
- Frutas coleccionables de al menos 3 tipos, con distinto puntaje según el tipo.
- Bonus de inmunidad temporal por recolección de frutas (cantidad/tipo o dentro de una ventana de tiempo).
- Monstruos que patrullan por puntos libres cercanos a su posición inicial, elegidos al azar y recorridos con pathfinding; a partir del segundo nivel, monstruos con área de detección y persecución temporal.
- Sistema de 5 vidas.
- Sistema de puntuación.
- Bonus de 100 puntos por victoria final.
- Bonus de 50 puntos por vida sobrante en victoria final.
- Bonus de 5 puntos por segundo sobrante en victoria final.
- Condición de victoria únicamente al completar todos los niveles.
- Condición de derrota mediante pérdida de todas las vidas o agotamiento del tiempo en cualquier nivel.
- Registro de puntaje exclusivamente en caso de Victoria final (no en Game Over ni al completar un nivel intermedio).
- Menú principal.
- Tabla de puntuaciones Top 10.
- Registro de nombre y puntuación.
- Base de datos SQLite local.
- Pantalla de resultado y pantalla final.
- Funcionamiento completamente offline.
- Versión ejecutable para Windows mediante archivo `.exe`.

## Funcionalidades fuera del alcance inicial

Las siguientes funcionalidades no forman parte de la primera versión:

- Más de 2 niveles (podrán evaluarse según el tiempo disponible de desarrollo).
- Inteligencia artificial avanzada para los monstruos (más allá del patrón de recorrido y la persecución por área desde el segundo nivel).
- Generación aleatoria/procedural del trazado de los laberintos (solo se sortea aleatoriamente qué semilla prediseñada se utiliza).

Estas funcionalidades podrán considerarse para futuras versiones si el tiempo disponible para el proyecto lo permite.
