# Roadmap de desarrollo — Maze Level One Game

---

## Etapa 1 — Cámara y base de movimiento

1.1. **Sistema de seguimiento de cámara**: el jugador queda fijo en el centro de la pantalla; al moverse, se desplaza el mundo/mapa en sentido contrario, generando la sensación de recorrido.
1.2. **Límites del mundo**: definir el tamaño total del mapa para que la cámara no muestre zonas fuera de sus bordes.
1.3. **Movimiento en coordenadas de mundo**: adaptar el movimiento y el `clamp` actuales para que trabajen sobre la posición del jugador dentro del mapa, no de la pantalla.

## Etapa 2 — Pantallas y flujo del juego

2.1. **Máquina de estados de pantallas**: estructura simple para alternar entre Inicio, Juego, Resultado, Ranking y Final.
2.2. **Pantalla de Inicio**: título y opciones Jugar / Instrucciones / Tabla de puntos / Salir.
2.3. **Pantalla de Instrucciones**: texto breve de controles y objetivo, con vuelta al menú.
2.4. **Pantalla de Juego**: integrar la cámara y el jugador desarrollados en la Etapa 1 dentro de este estado.

## Etapa 3 — Laberinto y colisiones

3.1. **Representación del laberinto**: definir el mapa como grilla/matriz de paredes y caminos.
3.2. **Colisión con paredes**: impedir que el jugador atraviese las celdas marcadas como pared.
3.3. **Dibujo del laberinto con cámara**: renderizar solo la porción visible del laberinto según la posición de la cámara.
3.4. **Semillas de laberinto**: cargar 3 semillas prediseñadas por nivel y elegir una al azar al iniciar/reiniciar.

## Etapa 4 — Frutas, vidas y monstruos

4.1. **Frutas coleccionables**: distintos tipos con distinto puntaje, ubicadas en posiciones fijas del laberinto (incluyendo zonas fuera del camino principal).
4.2. **Sistema de vidas**: 5 vidas iniciales, con período de invulnerabilidad tras recibir daño.
4.3. **Monstruos con patrón fijo**: recorrido predefinido de ida y vuelta, con colisión que resta una vida.
4.4. **Bonus de inmunidad**: activación temporal al recolectar cierta cantidad/tipo de frutas, bloqueando el daño de monstruos.
4.5. **Monstruos con área de persecución** (nivel 2+): detección de cercanía del jugador y regreso a su patrón por defecto al perderlo.

## Etapa 5 — Progresión, tiempo y condiciones de fin

5.1. **Tiempo límite por nivel**: cuenta regresiva visible en el HUD.
5.2. **Salida del laberinto**: detectar contacto del jugador con la salida de cada nivel.
5.3. **Avance entre niveles**: al completar un nivel no final, pasar al siguiente conservando vidas y puntaje, reiniciando tiempo y semilla.
5.4. **Condiciones de fin de partida**: Game Over por vidas en 0 o tiempo agotado; Victoria solo al completar el último nivel.
5.5. **Cálculo de bonus final**: sumar 100 pts de victoria + 50 pts por vida restante + 5 pts por segundo sobrante.

## Etapa 6 — Persistencia, ranking y cierre

6.1. **Pantalla de Resultado**: mostrar Victoria o Game Over con el puntaje obtenido.
6.2. **Registro en SQLite**: solicitar nombre y guardar puntaje únicamente en caso de Victoria.
6.3. **Pantalla de Ranking y Pantalla Final**: Top 10 de puntajes, con opciones de jugar de nuevo o volver al menú.
6.4. **Cierre de recursos**: liberar correctamente la conexión a la base de datos al salir del juego.
6.5. **Empaquetado final**: generar el ejecutable `.exe` para Windows.
