"""Pantalla de juego: movimiento, frutas, monstruos y salida del nivel."""

import math
import random

import pygame

from src.constants import (
    ALTO_PANTALLA,
    ANCHO_PANTALLA,
    COLOR_FONDO,
    COLOR_JUGADOR,
    COLOR_MONSTRUO,
    COLOR_SALIDA,
    DISTANCIA_MINIMA_SPAWN,
    DURACION_INMUNIDAD,
    DURACION_INVULNERABILIDAD,
    FRUTAS_PARA_INMUNIDAD,
    HUD_HEIGHT,
    PUNTOS_PATRULLA,
    RADIO_PATRULLA,
    VELOCIDAD_JUGADOR,
    VENTANA_INMUNIDAD,
)
from src.entities.fruit import Fruit
from src.entities.monster import Monster
from src.entities.player import Player
from src.estados import EstadoJuego
from src.scoring import calcular_bonus
from src.ui.hud import dibujar_hud
from src.world.camera import Camera
from src.world.maze import Maze
from src.world.placement import elegir_posiciones, generar_patrulla
from src.world.seeds import (
    FRUTAS_POR_NIVEL,
    MONSTRUOS_POR_NIVEL,
    NIVELES,
)

ENTRADA_SALIDA_MINIMA = 0.70
DURACION_EFECTO_VICTORIA = 1.4
INTERVALO_PASO = 0.30


class GameScreen:
    """Ejecuta la partida y dibuja el laberinto y sus entidades."""

    def __init__(self):
        self.maze = None
        self.camera = None
        self.player = None
        self.frutas = []
        self.monstruos = []
        self.salida = None
        self.tiempo_nivel = 0
        self.tiempo_base = 0
        self.tiempo_extra = 0
        self.frutas_recolectadas_ventana = []
        self.inmune = False
        self.tiempo_inmunidad = 0
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 0
        self.efecto_victoria = None
        self._capa_efecto = None
        self.tiempo_paso = 0.0
        self._mundo_rect = pygame.Rect(0, 0, 0, 0)

    def handle_event(self, game, event):
        """Vuelve al menú al presionar ESC; el resto lo resuelve el bucle."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return EstadoJuego.MENU
        return None

    def cargar_nivel(self, nivel, tiempo_extra=0):
        """Prepara el laberinto, el jugador, las frutas y los monstruos."""
        self.maze = Maze(nivel)
        self.camera = Camera(
            self.maze.ancho,
            self.maze.alto,
            ANCHO_PANTALLA,
            ALTO_PANTALLA,
        )
        self._mundo_rect = pygame.Rect(0, 0, self.maze.ancho, self.maze.alto)

        self.player = Player(
            self.maze.spawn.centerx - 25,
            self.maze.spawn.centery - 25,
        )

        posiciones_frutas, posiciones_monstruos = (
            self._elegir_posiciones_nivel(nivel)
        )
        self.frutas = self._crear_frutas(nivel, posiciones_frutas)
        self.monstruos = self._crear_monstruos(nivel, posiciones_monstruos)
        self._configurar_salida(nivel, tiempo_extra)
        self._reiniciar_temporizadores()
        self.camera.update(self.player.rect)

    def _elegir_posiciones_nivel(self, nivel):
        """Sortea posiciones únicas y lejos del spawn para las entidades."""
        disponibles = self.maze.obtener_posiciones_libres()
        evitar = [self.maze.spawn.center]
        posiciones_frutas = elegir_posiciones(
            disponibles,
            len(FRUTAS_POR_NIVEL[nivel]),
            evitar,
            DISTANCIA_MINIMA_SPAWN,
        )
        posiciones_monstruos = elegir_posiciones(
            disponibles,
            len(MONSTRUOS_POR_NIVEL[nivel]),
            [*evitar, self.maze.salida.center],
            DISTANCIA_MINIMA_SPAWN,
        )
        return posiciones_frutas, posiciones_monstruos

    def _crear_frutas(self, nivel, posiciones):
        """Crea las frutas del nivel en las posiciones sorteadas."""
        return [
            Fruit(
                x - 16,
                y - 16,
                tipo=datos["tipo"],
                color=datos["color"],
                puntos=datos["puntos"],
            )
            for datos, (x, y) in zip(
                FRUTAS_POR_NIVEL[nivel], posiciones
            )
        ]

    def _crear_monstruos(self, nivel, posiciones):
        """Crea los monstruos con una patrulla local a su posición."""
        monstruos = []
        for datos, (x, y) in zip(MONSTRUOS_POR_NIVEL[nivel], posiciones):
            celda = (x // self.maze.tile_size, y // self.maze.tile_size)
            patrulla = generar_patrulla(
                self.maze,
                celda,
                PUNTOS_PATRULLA,
                RADIO_PATRULLA,
            )
            monstruos.append(
                Monster(
                    x - datos["ancho"] // 2,
                    y - datos["alto"] // 2,
                    datos["ancho"],
                    datos["alto"],
                    patrulla,
                    datos["velocidad"],
                    datos.get("rango_deteccion", 0),
                )
            )
        return monstruos

    def _configurar_salida(self, nivel, tiempo_extra=0):
        """Toma la salida del mapa y fija el tiempo base más lo acumulado."""
        self.salida = self.maze.salida
        self.tiempo_base = NIVELES[nivel]["tiempo"]
        self.tiempo_extra = max(0.0, float(tiempo_extra))
        self.tiempo_nivel = self.tiempo_base + self.tiempo_extra

    def _reiniciar_temporizadores(self):
        """Reinicia los efectos temporales al empezar un nivel."""
        self.frutas_recolectadas_ventana = []
        self.inmune = False
        self.tiempo_inmunidad = 0
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 0
        self.efecto_victoria = None
        self.tiempo_paso = 0.0

    def _proporcion_dentro_salida(self, jugador_rect):
        interseccion = jugador_rect.clip(self.salida)
        area_jugador = jugador_rect.width * jugador_rect.height
        if area_jugador <= 0:
            return 0.0
        area_dentro = interseccion.width * interseccion.height
        return area_dentro / area_jugador

    def _terminar_partida(self, juego):
        """Cierra la partida como Game Over y devuelve el próximo estado."""
        juego.mensaje_resultado = "Game Over"
        juego.puntaje_final = juego.puntaje
        juego.audio.reproducir("game_over")
        return EstadoJuego.RESULTADO

    def _iniciar_efecto_victoria(self):
        cx, cy = self.salida.center
        particulas = []
        for _ in range(90):
            angulo = random.uniform(0, math.tau)
            velocidad = random.uniform(70, 340)
            vida = random.uniform(0.55, 1.25)
            particulas.append(
                {
                    "x": cx + random.uniform(-18, 18),
                    "y": cy + random.uniform(-18, 18),
                    "vx": math.cos(angulo) * velocidad,
                    "vy": math.sin(angulo) * velocidad - 45,
                    "radio": random.choice((2, 2, 2, 3, 3, 4)),
                    "color": random.choice(
                        (
                            (255, 214, 92),
                            (255, 238, 170),
                            (255, 250, 235),
                            (150, 225, 120),
                        )
                    ),
                    "vida": vida,
                    "vida_max": vida,
                }
            )
        self.efecto_victoria = {"tiempo": 0.0, "particulas": particulas}

    def _actualizar_efecto_victoria(self, dt):
        efecto = self.efecto_victoria
        efecto["tiempo"] += dt
        arrastre = max(0.0, 1.0 - 2.1 * dt)

        for particula in efecto["particulas"]:
            particula["x"] += particula["vx"] * dt
            particula["y"] += particula["vy"] * dt
            particula["vx"] *= arrastre
            particula["vy"] = particula["vy"] * arrastre + 95 * dt
            particula["vida"] -= dt

        efecto["particulas"] = [
            particula
            for particula in efecto["particulas"]
            if particula["vida"] > 0
        ]

        if efecto["tiempo"] >= DURACION_EFECTO_VICTORIA:
            self.efecto_victoria = None

    def _dibujar_efecto_victoria(self, pantalla):
        efecto = self.efecto_victoria
        if efecto is None:
            return

        capa = self._obtener_capa_efecto()
        capa.fill((0, 0, 0, 0))

        tiempo = efecto["tiempo"]
        cx = self.salida.centerx - self.camera.x
        cy = self.salida.centery - self.camera.y + HUD_HEIGHT

        self._dibujar_destello(capa, tiempo)
        self._dibujar_brillo_salida(capa, tiempo, cx, cy)
        self._dibujar_ondas(capa, tiempo, cx, cy)
        self._dibujar_particulas(capa, efecto["particulas"])

        pantalla.blit(capa, (0, 0))

    def _obtener_capa_efecto(self):
        """Devuelve la superficie reutilizable del efecto de victoria."""
        if self._capa_efecto is None:
            self._capa_efecto = pygame.Surface(
                (ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA
            )
        return self._capa_efecto

    def _dibujar_destello(self, capa, tiempo):
        """Dibuja el destello inicial del efecto."""
        alpha_destello = int(70 * max(0.0, 1.0 - tiempo / 0.35))
        if alpha_destello > 0:
            capa.fill((255, 232, 160, alpha_destello))

    def _dibujar_brillo_salida(self, capa, tiempo, cx, cy):
        """Dibuja el brillo pulsante alrededor de la salida."""
        progreso = min(1.0, tiempo / DURACION_EFECTO_VICTORIA)
        alpha_salida = int(120 * (1.0 - progreso))
        if alpha_salida <= 0:
            return

        pulso = int(4 + 4 * math.sin(tiempo * math.pi * 8))
        brillo = pygame.Rect(0, 0, self.salida.width, self.salida.height)
        brillo.center = (cx, cy)
        pygame.draw.rect(
            capa,
            (255, 238, 170, alpha_salida),
            brillo.inflate(10 + pulso, 10 + pulso),
            3,
            border_radius=10,
        )

    def _dibujar_ondas(self, capa, tiempo, cx, cy):
        """Dibuja las ondas expansivas del efecto."""
        for i in range(3):
            progreso = (tiempo - i * 0.14) / 0.95
            if not 0.0 <= progreso <= 1.0:
                continue
            radio = int(20 + 210 * progreso)
            alpha_onda = int(170 * (1.0 - progreso))
            color = (255, 238, 170) if i % 2 == 0 else (255, 214, 92)
            pygame.draw.circle(
                capa, (*color, alpha_onda), (cx, cy), radio, 3
            )

    def _dibujar_particulas(self, capa, particulas):
        """Dibuja las partículas del efecto de victoria."""
        for particula in particulas:
            px = particula["x"] - self.camera.x
            py = particula["y"] - self.camera.y + HUD_HEIGHT
            if not -20 <= px <= ANCHO_PANTALLA + 20:
                continue
            if not -20 <= py <= ALTO_PANTALLA + 20:
                continue

            proporcion_vida = max(
                0.0, particula["vida"] / particula["vida_max"]
            )
            alpha = int(255 * min(1.0, proporcion_vida * 1.8))
            radio = max(
                1, int(particula["radio"] * (0.5 + 0.5 * proporcion_vida))
            )
            color = (*particula["color"], alpha)
            pygame.draw.circle(
                capa,
                (255, 240, 190, max(1, alpha // 5)),
                (px, py),
                radio + 3,
            )
            pygame.draw.circle(capa, color, (px, py), radio)

    def _actualizar_temporizadores(self, dt):
        if self.inmune:
            self.tiempo_inmunidad -= dt
            if self.tiempo_inmunidad <= 0:
                self.inmune = False

        if self.invulnerable:
            self.tiempo_invulnerabilidad -= dt
            if self.tiempo_invulnerabilidad <= 0:
                self.invulnerable = False

    def _mover_jugador(self, dt):
        keys = pygame.key.get_pressed()
        direccion = pygame.math.Vector2(
            int(keys[pygame.K_RIGHT] or keys[pygame.K_d])
            - int(keys[pygame.K_LEFT] or keys[pygame.K_a]),
            int(keys[pygame.K_DOWN] or keys[pygame.K_s])
            - int(keys[pygame.K_UP] or keys[pygame.K_w]),
        )
        if direccion.length_squared() > 0:
            direccion = direccion.normalize()
        movimiento = direccion * VELOCIDAD_JUGADOR * dt

        posicion_anterior = self.player.rect.topleft
        self.player.mover(
            movimiento.x, movimiento.y, self.maze, self._mundo_rect
        )
        self.player.update(dt)

        if self.player.rect.topleft != posicion_anterior:
            self.tiempo_paso -= dt
            if self.tiempo_paso <= 0:
                self.tiempo_paso = INTERVALO_PASO
                return True
        else:
            self.tiempo_paso = 0.0
        return False

    def _recolectar_frutas(self, juego):
        for fruta in self.frutas:
            if fruta.activa and self.player.rect.colliderect(fruta.rect):
                juego.puntaje += fruta.recolectar()
                juego.audio.reproducir("collect")
                ahora = pygame.time.get_ticks() / 1000.0
                self.frutas_recolectadas_ventana.append(ahora)
                self.frutas_recolectadas_ventana = [
                    instante
                    for instante in self.frutas_recolectadas_ventana
                    if ahora - instante <= VENTANA_INMUNIDAD
                ]
                if (
                    len(self.frutas_recolectadas_ventana)
                    >= FRUTAS_PARA_INMUNIDAD
                ):
                    self.inmune = True
                    self.tiempo_inmunidad = DURACION_INMUNIDAD
                    self.frutas_recolectadas_ventana = []
                    juego.audio.reproducir("inmune")

    def _actualizar_monstruos(self, dt):
        for monstruo in self.monstruos:
            monstruo.update(dt, self.player.rect, self.maze, self._mundo_rect)

    def _aplicar_dano(self, juego):
        if self.inmune or self.invulnerable:
            return None

        for monstruo in self.monstruos:
            if self.player.rect.colliderect(monstruo.rect):
                juego.vidas = max(0, juego.vidas - 1)
                juego.audio.reproducir("damage")
                # Solo los monstruos que persiguen se detienen tras golpear.
                if monstruo.rango_deteccion > 0:
                    monstruo.pausar_tras_dano()
                self.invulnerable = True
                self.tiempo_invulnerabilidad = DURACION_INVULNERABILIDAD
                if juego.vidas <= 0:
                    return self._terminar_partida(juego)
                break
        return None

    def _comprobar_salida(self, juego):
        if (
            self._proporcion_dentro_salida(self.player.rect)
            < ENTRADA_SALIDA_MINIMA
        ):
            return

        if juego.nivel_actual < len(NIVELES) - 1:
            tiempo_extra = max(0, int(self.tiempo_nivel))
            juego.cargar_nivel(juego.nivel_actual + 1, tiempo_extra)
            return

        bonus = calcular_bonus(juego.vidas, self.tiempo_nivel)
        juego.puntaje_final = juego.puntaje + bonus
        juego.mensaje_resultado = "Victoria"
        juego.audio.reproducir("success_level")
        self._iniciar_efecto_victoria()

    def update(self, juego, dt):
        """Avanza la partida y devuelve el próximo estado, o None."""
        if juego.estado != EstadoJuego.JUEGO:
            return None

        if self.efecto_victoria is not None:
            self._actualizar_efecto_victoria(dt)
            if self.efecto_victoria is not None:
                return None
            juego.audio.reproducir("final_victory")
            return EstadoJuego.INGRESO_NOMBRE

        self._actualizar_temporizadores(dt)

        self.tiempo_nivel -= dt
        if self.tiempo_extra > 0:
            self.tiempo_extra = max(0.0, self.tiempo_extra - dt)
        if self.tiempo_nivel <= 0:
            self.tiempo_nivel = 0
            self.tiempo_extra = 0
            return self._terminar_partida(juego)

        if self._mover_jugador(dt):
            juego.audio.reproducir_paso()

        self._recolectar_frutas(juego)
        self._actualizar_monstruos(dt)

        resultado = self._aplicar_dano(juego)
        if resultado:
            return resultado

        return self._comprobar_salida(juego)

    def draw(self, juego):
        """Dibuja el laberinto, la salida, las entidades, el efecto y el HUD."""
        self.camera.update(self.player.rect)
        pantalla = juego.pantalla
        pantalla.fill(COLOR_FONDO)

        self.maze.dibujar(pantalla, self.camera, offset_y=HUD_HEIGHT)
        self._dibujar_salida(pantalla)
        self._dibujar_frutas(pantalla)
        self._dibujar_jugador(pantalla)
        self._dibujar_monstruos(pantalla)
        self._dibujar_efecto_victoria(pantalla)
        dibujar_hud(
            pantalla,
            juego.vidas,
            juego.puntaje,
            self.tiempo_nivel,
            juego.nivel_actual,
            self.inmune,
            self.tiempo_extra,
        )

    def _dibujar_salida(self, pantalla):
        """Dibuja el borde visible de la salida del nivel."""
        salida_pantalla = self.camera.aplicar(self.salida)
        pygame.draw.rect(
            pantalla, COLOR_SALIDA, salida_pantalla, 4, border_radius=10
        )

    def _dibujar_frutas(self, pantalla):
        """Dibuja las frutas activas."""
        for fruta in self.frutas:
            if not fruta.activa:
                continue
            fruta_pantalla = self.camera.aplicar(fruta.rect)
            sprite = fruta.get_sprite()
            if sprite:
                float_y = fruta.get_float_offset()
                pantalla.blit(
                    sprite,
                    (fruta_pantalla.x, fruta_pantalla.y + float_y),
                )
            else:
                pygame.draw.rect(pantalla, fruta.color, fruta_pantalla)

    def _dibujar_jugador(self, pantalla):
        """Dibuja al jugador, parpadeando mientras es invulnerable."""
        if self.invulnerable and int(pygame.time.get_ticks() / 100) % 2 != 0:
            return

        jugador_pantalla = self.camera.aplicar(self.player.rect)
        sprite = self.player.get_current_sprite()
        if sprite:
            offset_x, offset_y = self.player.get_draw_offset()
            pantalla.blit(
                sprite,
                (jugador_pantalla.x - offset_x, jugador_pantalla.y - offset_y),
            )
        else:
            color = (0, 255, 0) if self.inmune else COLOR_JUGADOR
            pygame.draw.rect(pantalla, color, jugador_pantalla)

    def _dibujar_monstruos(self, pantalla):
        """Dibuja todos los monstruos del nivel."""
        for monstruo in self.monstruos:
            monstruo_pantalla = self.camera.aplicar(monstruo.rect)
            sprite = monstruo.get_current_sprite()
            if sprite:
                offset_x, offset_y = monstruo.get_draw_offset()
                pantalla.blit(
                    sprite,
                    (
                        monstruo_pantalla.x - offset_x,
                        monstruo_pantalla.y - offset_y,
                    ),
                )
            else:
                pygame.draw.rect(pantalla, COLOR_MONSTRUO, monstruo_pantalla)
