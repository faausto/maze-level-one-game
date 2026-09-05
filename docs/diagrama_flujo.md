# Diagrama de flujo de pantallas

## Flujo general

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

## Detalle de cada pantalla

### 1. Menú Principal

**Opciones:**
- Jugar
- Instrucciones
- Tabla de puntos
- Salir

**Comportamiento:**
- `Jugar`: Inicia una nueva partida reiniciando nivel, vidas y puntaje, y transiciona a la pantalla de Juego.
- `Instrucciones`: Muestra la pantalla de Instrucciones.
- `Tabla de puntos`: Carga y muestra el ranking de puntuaciones almacenadas.
- `Salir`: Cierra la aplicación.
- Durante el juego, al presionar `ESC` se regresa a este menú.

### 2. Instrucciones

**Contenido:**
- Controles: W A S D o flechas
- Objetivo: encontrar la salida del laberinto
- Recolectar frutas para sumar puntos
- Evitar los monstruos
- Cantidad de vidas por partida
- Condición de tiempo por nivel

**Transiciones:**
- `ESC` → Vuelve al Menú Principal

### 3. Juego

**Estados internos:**
- Nivel actual (0 a N-1)
- Vidas (cantidad inicial definida)
- Puntaje acumulado
- Tiempo restante del nivel
- Efectos temporales: inmunidad (por recolección de frutas) e invulnerabilidad (por colisión con monstruo)

**Mecánicas:**
- Movimiento del jugador
- Recolección de frutas y sumar puntos
- Evasión de monstruos
- Objetivo intermedio para progresar
- Salida de nivel

**Transiciones:**
- `Salida de nivel intermedio` → Carga el siguiente nivel en la misma pantalla de Juego.
- `Salida del último nivel` → Calcula puntaje final con bonus y transiciona a Ingreso de Nombre.
- `Colisión con monstruo` (sin inmunidad) → Reduce vidas y activa invulnerabilidad temporal.
- `Vidas <= 0` → Genera resultado "Game Over" y transiciona a Pantalla Resultado.
- `Tiempo agotado` → Genera resultado "Game Over" y transiciona a Pantalla Resultado.
- `ESC` → Vuelve al Menú Principal.

### 4. Resultado

**Contenido:**
- Mensaje de resultado: "Victoria" o "Game Over"
- Puntaje final de la partida

**Transiciones:**
- `ENTER` → Avanza a la Pantalla Final.

### 5. Ingreso de Nombre

**Condición:** Se muestra únicamente cuando el resultado es "Victoria".

**Contenido:**
- Campo de texto para ingresar nombre del jugador

**Transiciones:**
- `ENTER` (con nombre válido) → Guarda el puntaje en SQLite y transiciona a la Pantalla Final.
- `ESC` → Transiciona a la Pantalla Final sin guardar.
- `BACKSPACE` → Borra el último carácter del nombre.

### 6. Pantalla Final

**Contenido:**
- Mensaje de resultado: "Victoria" o "Game Over"
- Puntaje final
- Opciones de navegación: "Jugar de nuevo" / "Volver al menú"

**Transiciones:**
- `Jugar de nuevo` → Reinicia la partida y transiciona a Juego.
- `Volver al menú` → Regresa al Menú Principal.

### 7. Ranking

**Contenido:**
- Listado de Top 10 puntuaciones registradas en SQLite
- Formato: posición, nombre y puntaje

**Transiciones:**
- `ESC` → Vuelve al Menú Principal.

## Consideraciones de diseño

- **Base de datos:** Se utilizará SQLite para persistir los puntajes y nombres de los jugadores.
- **Puntaje final (Victoria):** Estará compuesto por el puntaje acumulado más un bonus calculado según vidas restantes y tiempo sobrante.
- **Puntaje final (Game Over):** Solo considerará el puntaje acumulado sin bonus adicional.
- **Vidas:** Se definirá una cantidad inicial por partida y se restarán al colisionar con monstruos.
- **Efectos temporales:** Se contemplan estados de inmunidad e invulnerabilidad con duraciones limitadas.
- **Niveles:** El juego contará con múltiples niveles definidos en configuración, cada uno con su propio tiempo, frutas y monstruos.
