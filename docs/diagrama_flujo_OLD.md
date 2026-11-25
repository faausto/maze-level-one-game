# Diagrama de flujo de pantallas

## Flujo general

```
Inicio (Menú principal)
   │
   ├── Instrucciones ──► (volver a Inicio con ESC)
   ├── Tabla de puntos (Ranking) ──► (volver a Inicio con ESC)
   └── Jugar
          │
          ▼
       Juego (Nivel actual)
          │
          ├── Alcanza salida de nivel intermedio ──► avanza al siguiente nivel (vuelve a "Juego")
          ├── Alcanza salida del último nivel ──► Resultado: Victoria ──► Ingreso de nombre ──► Registro en SQLite ──► Pantalla Final ──► Jugar de nuevo / Volver al menú
          ├── Pierde 5 vidas ──► Resultado: Game Over ──► Pantalla Final ──► Jugar de nuevo / Volver al menú
          └── Se agota el tiempo ──► Resultado: Game Over ──► Pantalla Final ──► Jugar de nuevo / Volver al menú
```

## Detalle de cada pantalla

### 1. Menú Principal

**Archivo:** `src/screens/menu.py`

**Opciones:**
- Jugar
- Instrucciones
- Tabla de puntos
- Salir

**Transiciones:**
- `Jugar` → Reinicia la partida (nivel 0, 5 vidas, puntaje 0) → `Juego`
- `Instrucciones` → `Instrucciones`
- `Tabla de puntos` → Carga el ranking → `Ranking`
- `Salir` → Cierra el juego
- `ESC` (durante el juego) → Vuelve al menú principal

### 2. Instrucciones

**Archivo:** `src/screens/instructions.py`

**Contenido:**
- Controles: W A S D o flechas
- Objetivo: encuentra la salida del laberinto
- Recolecta frutas para sumar puntos
- Evita los monstruos
- Tienes 5 vidas por partida
- Completa los niveles antes del tiempo

**Transiciones:**
- `ESC` → Vuelve al `Menú Principal`

### 3. Juego

**Archivo:** `src/screens/game_screen.py`

**Estados internos:**
- Nivel actual (0 a N-1)
- Vidas (5 iniciales)
- Puntaje
- Tiempo restante del nivel
- Inmunidad temporal (al recolectar 3 frutas en 10 segundos)
- Invulnerabilidad temporal (despuÃ©s de colisión con monstruo)

**Mecánicas:**
- Movimiento con WASD o flechas
- Recolección de frutas (puntos)
- Evasión de monstruos
- Objetivo intermedio (recolectar para avanzar)
- Salida de nivel

**Transiciones:**
- `Salida de nivel intermedio` → Carga siguiente nivel → `Juego` (misma pantalla)
- `Salida del último nivel` → Calcula bonus (100 + vidas * 50 + tiempo * 5) → `Ingreso de Nombre`
- `Colisión con monstruo` (sin inmunidad) → Pierde 1 vida, activa invulnerabilidad de 1s
- `Vidas <= 0` → `Resultado: Game Over` → `Resultado`
- `Tiempo agotado` → `Resultado: Game Over` → `Resultado`
- `ESC` → Vuelve al `Menú Principal`

### 4. Resultado

**Archivo:** `src/screens/result.py`

**Contenido:**
- Mensaje: "Victoria" o "Game Over"
- Puntaje final

**Transiciones:**
- `ENTER` → `Pantalla Final`

### 5. Ingreso de Nombre

**Archivo:** `src/screens/name_input.py`

**Condición:** Solo se muestra cuando el resultado es "Victoria"

**Contenido:**
- Campo de texto para ingresar nombre (máximo 15 caracteres)
- Opción de guardar o cancelar

**Transiciones:**
- `ENTER` (con nombre válido) → Guarda puntaje en SQLite → Carga ranking → `Pantalla Final`
- `ESC` → `Pantalla Final` (sin guardar)
- `BACKSPACE` → Borra último caracter

### 6. Pantalla Final

**Archivo:** `src/screens/final.py`

**Contenido:**
- Mensaje: "Victoria" o "Game Over"
- Puntaje final
- Opciones: "Jugar de nuevo" / "Volver al menú"

**Transiciones:**
- `Jugar de nuevo` → Reinicia partida → `Juego`
- `Volver al menú` → `Menú Principal`

### 7. Ranking

**Archivo:** `src/screens/ranking.py`

**Contenido:**
- Top 10 puntuaciones registradas en SQLite
- Formato: `#. Nombre - Puntaje`

**Transiciones:**
- `ESC` → Vuelve al `Menú Principal`

## Estados del juego

Definidos en `src/game.py`:

```python
class EstadoJuego:
    MENU = "menu"
    INSTRUCCIONES = "instrucciones"
    JUEGO = "juego"
    RESULTADO = "resultado"
    RANKING = "ranking"
    FINAL = "final"
    INGRESO_NOMBRE = "ingreso_nombre"
```

## Estructura de archivos de pantallas

```
src/screens/
├── menu.py           # Menú principal
├── instructions.py   # Instrucciones
├── game_screen.py    # Pantalla de juego
├── result.py         # Pantalla de resultado (transición)
├── name_input.py     # Ingreso de nombre (solo victoria)
├── ranking.py        # Ranking/Top 10
└── final.py          # Pantalla final
```

## Notas adicionales

- **Base de datos:** SQLite, almacenada en `database/ranking.db`
- **Puntaje final (Victoria):** `puntaje + bonus` donde `bonus = 100 + vidas * 50 + tiempo_restante * 5`
- **Puntaje final (Game Over):** Solo el puntaje acumulado (sin bonus)
- **Vidas:** 5 por partida, se pierden al colisionar con monstruos
- **Inmunidad:** Se activa al recolectar 3 frutas en 10 segundos (dura 5 segundos)
- **Invulnerabilidad:** 1 segundo después de cada colisión con monstruo
- **Niveles:** Múltiples niveles definidos en `src/constants.py` (NIVELES, FRUTAS_POR_NIVEL, MONSTRUOS_POR_NIVEL, SALIDAS)
