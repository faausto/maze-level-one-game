import pygame
import random
import math
from src.constants import (
    COLOR_FONDO,
    COLOR_OBJETIVO,
    COLOR_JUGADOR,
    COLOR_MONSTRUO,
    COLOR_TITULO,
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    HUD_HEIGHT,
    TILE_SIZE,
    VELOCIDAD_JUGADOR,
    FRUTAS_POR_NIVEL,
    MONSTRUOS_POR_NIVEL,
    SALIDAS,
    NIVELES,
)
from src.ui import fonts
from src.world.maze import Maze
from src.world.camera import Camera
from src.entities.player import Player
from src.entities.monster import Monster
from src.entities.fruit import Fruit
from src.ui.hud import dibujar_hud

ENTRADA_SALIDA_MINIMA = 0.70
PUNTOS_POR_FRUTA = 10
PUNTOS_POR_VIDA = 20
PUNTOS_POR_SEGUNDO = 2
DURACION_EFECTO_VICTORIA = 1.4


class GameScreen:
    def __init__(self):
        self.maze = None
        self.camera = None
        self.player = None
        self.frutas = []
        self.monstruos = []
        self.salida = None
        self.tiempo_nivel = 0
        self.frutas_recolectadas_ventana = []
        self.inmune = False
        self.tiempo_inmunidad = 0
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 0
        self.efecto_victoria = None
        self._capa_efecto = None

    def cargar_nivel(self, nivel, juego):
        self.maze = Maze(nivel)
        self.camera = Camera(self.maze.ancho, self.maze.alto, ANCHO_PANTALLA, ALTO_PANTALLA)
        mundo_rect = pygame.Rect(0, 0, self.maze.ancho, self.maze.alto)
        posiciones = self.maze.obtener_posiciones_libres()

        spawn = posiciones[0] if posiciones else (64, 64)
        self.player = Player(spawn[0] - 25, spawn[1] - 25)

        objetivo_pos = posiciones[1] if len(posiciones) > 1 else (spawn[0] + 128, spawn[1])
        juego.objetivo = pygame.Rect(objetivo_pos[0] - 25, objetivo_pos[1] - 25, 51, 51)

        self.frutas = []
        fruta_data = FRUTAS_POR_NIVEL[nivel]
        posiciones_disponibles = posiciones[2:] if len(posiciones) > 2 else posiciones[:]
        random.shuffle(posiciones_disponibles)
        for i, f in enumerate(fruta_data):
            if i < len(posiciones_disponibles):
                pos = posiciones_disponibles[i]
                self.frutas.append(Fruit(pos[0] - 16, pos[1] - 16, tipo=f["tipo"], color=f["color"], puntos=f["puntos"]))
            else:
                self.frutas.append(Fruit(f["x"], f["y"], tipo=f["tipo"], color=f["color"], puntos=f["puntos"]))

        self.monstruos = []
        posiciones_libres = self.maze.obtener_posiciones_libres()
        if len(posiciones_libres) > 6:
            monster_positions = posiciones_libres[len(posiciones_libres) // 2:len(posiciones_libres) // 2 + 6]
        else:
            monster_positions = posiciones_libres[2:6] if len(posiciones_libres) > 2 else []
        random.shuffle(monster_positions)
        for idx, m in enumerate(MONSTRUOS_POR_NIVEL[nivel]):
            if idx < len(monster_positions):
                pos = monster_positions[idx]
                self.monstruos.append(
                    Monster(
                        pos[0] - m["ancho"] // 2,
                        pos[1] - m["alto"] // 2,
                        m["ancho"],
                        m["alto"],
                        m["puntos"],
                        m["velocidad"],
                        m.get("rango_deteccion", 0),
                    )
                )
            else:
                self.monstruos.append(
                    Monster(
                        m["x"],
                        m["y"],
                        m["ancho"],
                        m["alto"],
                        m["puntos"],
                        m["velocidad"],
                        m.get("rango_deteccion", 0),
                    )
                )
        for monster in self.monstruos:
            monster.objetivo_wander = None
            monster.origen_wander = (monster.rect.x, monster.rect.y)
            monster.distancia_recorrida = 0
            monster.max_distancia = random.randint(102, 205)
            if self.maze:
                monster._generar_objetivo_wander(self.maze)

        salida = SALIDAS[nivel]
        self.salida = pygame.Rect(salida["x"], salida["y"], salida["ancho"], salida["alto"])
        self.maze.abrir_zona(self.salida)
        self.tiempo_nivel = NIVELES[nivel]["tiempo"]
        self.frutas_recolectadas_ventana = []
        self.inmune = False
        self.tiempo_inmunidad = 0
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 0
        self.efecto_victoria = None

    def _proporcion_dentro_salida(self, jugador_rect):
        interseccion = jugador_rect.clip(self.salida)
        area_jugador = jugador_rect.width * jugador_rect.height
        if area_jugador <= 0:
            return 0.0
        area_dentro = interseccion.width * interseccion.height
        return area_dentro / area_jugador

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
            p for p in efecto["particulas"] if p["vida"] > 0
        ]

        if efecto["tiempo"] >= DURACION_EFECTO_VICTORIA:
            self.efecto_victoria = None

    def _dibujar_efecto_victoria(self, pantalla):
        efecto = self.efecto_victoria
        if efecto is None:
            return

        if self._capa_efecto is None:
            self._capa_efecto = pygame.Surface(
                (ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA
            )
        capa = self._capa_efecto
        capa.fill((0, 0, 0, 0))

        tiempo = efecto["tiempo"]
        t = min(1.0, tiempo / DURACION_EFECTO_VICTORIA)
        cx = self.salida.centerx - self.camera.x
        cy = self.salida.centery - self.camera.y + HUD_HEIGHT

        # Destello cálido inicial.
        alpha_destello = int(70 * max(0.0, 1.0 - tiempo / 0.35))
        if alpha_destello > 0:
            capa.fill((255, 232, 160, alpha_destello))

        # Resplandor del tile de salida.
        alpha_salida = int(120 * (1.0 - t))
        if alpha_salida > 0:
            pulso = int(4 + 4 * math.sin(tiempo * math.pi * 8))
            brillo = pygame.Rect(
                0, 0, self.salida.width, self.salida.height
            )
            brillo.center = (cx, cy)
            pygame.draw.rect(
                capa,
                (255, 238, 170, alpha_salida),
                brillo.inflate(10 + pulso, 10 + pulso),
                3,
                border_radius=10,
            )

        # Ondas doradas que se expanden.
        for i in range(3):
            progreso = (tiempo - i * 0.14) / 0.95
            if 0.0 <= progreso <= 1.0:
                radio = int(20 + 210 * progreso)
                alpha_onda = int(170 * (1.0 - progreso))
                color = (255, 238, 170) if i % 2 == 0 else (255, 214, 92)
                pygame.draw.circle(
                    capa, (*color, alpha_onda), (cx, cy), radio, 3
                )

        # Chispas doradas.
        for particula in efecto["particulas"]:
            px = particula["x"] - self.camera.x
            py = particula["y"] - self.camera.y + HUD_HEIGHT
            if px < -20 or px > ANCHO_PANTALLA + 20:
                continue
            if py < -20 or py > ALTO_PANTALLA + 20:
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
                capa, (255, 240, 190, max(1, alpha // 5)), (px, py), radio + 3
            )
            pygame.draw.circle(capa, color, (px, py), radio)

        pantalla.blit(capa, (0, 0))

    def update(self, juego, dt):
        if juego.estado != juego.estado_juego.JUEGO:
            return

        if self.efecto_victoria is not None:
            self._actualizar_efecto_victoria(dt)
            if self.efecto_victoria is None:
                juego.estado = juego.estado_juego.INGRESO_NOMBRE
            return

        if self.inmune:
            self.tiempo_inmunidad -= dt
            if self.tiempo_inmunidad <= 0:
                self.inmune = False

        if self.invulnerable:
            self.tiempo_invulnerabilidad -= dt
            if self.tiempo_invulnerabilidad <= 0:
                self.invulnerable = False

        self.tiempo_nivel -= dt
        if self.tiempo_nivel <= 0:
            self.tiempo_nivel = 0
            juego.mensaje_resultado = "Game Over"
            juego.puntaje_final = juego.puntaje
            juego.estado = juego.estado_juego.RESULTADO
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -VELOCIDAD_JUGADOR * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = VELOCIDAD_JUGADOR * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -VELOCIDAD_JUGADOR * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = VELOCIDAD_JUGADOR * dt

        mundo_rect = pygame.Rect(0, 0, self.maze.ancho, self.maze.alto)
        self.player.mover(dx, dy, self.maze, mundo_rect)
        self.player.update(dt)

        for fruta in self.frutas:
            if fruta.esta_activa() and self.player.get_rect().colliderect(fruta.get_rect()):
                fruta.recolectar()
                juego.puntaje += PUNTOS_POR_FRUTA
                ahora = pygame.time.get_ticks() / 1000.0
                self.frutas_recolectadas_ventana.append(ahora)
                self.frutas_recolectadas_ventana = [t for t in self.frutas_recolectadas_ventana if ahora - t <= 10]
                if len(self.frutas_recolectadas_ventana) >= 3:
                    self.inmune = True
                    self.tiempo_inmunidad = 5
                    self.frutas_recolectadas_ventana = []

        mundo_rect = pygame.Rect(0, 0, self.maze.ancho, self.maze.alto)
        for monstruo in self.monstruos:
            monstruo.update(dt, self.player.get_rect(), self.maze, mundo_rect)

        if not self.inmune and not self.invulnerable:
            for monstruo in self.monstruos:
                if self.player.get_rect().colliderect(monstruo.get_rect()):
                    juego.vidas -= 1
                    self.invulnerable = True
                    self.tiempo_invulnerabilidad = 1.0
                    if juego.vidas <= 0:
                        juego.mensaje_resultado = "Game Over"
                        juego.puntaje_final = juego.puntaje
                        juego.estado = juego.estado_juego.RESULTADO
                    break

        if self._proporcion_dentro_salida(self.player.get_rect()) >= ENTRADA_SALIDA_MINIMA:
            if juego.nivel_actual < len(NIVELES) - 1:
                juego.nivel_actual += 1
                self.cargar_nivel(juego.nivel_actual, juego)
            else:
                bonus = (
                    juego.vidas * PUNTOS_POR_VIDA
                    + int(self.tiempo_nivel) * PUNTOS_POR_SEGUNDO
                )
                juego.puntaje_final = juego.puntaje + bonus
                juego.mensaje_resultado = "Victoria"
                self._iniciar_efecto_victoria()

    def draw(self, juego):
        self.camera.update(self.player.get_rect())
        pantalla = juego.pantalla
        pantalla.fill(COLOR_FONDO)

        hud_height = HUD_HEIGHT
        self.maze.dibujar(pantalla, self.camera, offset_y=hud_height)

        for fruta in self.frutas:
            if fruta.esta_activa():
                fruta_pantalla = self.camera.aplicar(fruta.get_rect())
                sprite = fruta.get_sprite()
                if sprite:
                    float_y = fruta.get_float_offset()
                    sprite_scaled = pygame.transform.scale(sprite, (fruta_pantalla.width + 6, fruta_pantalla.height + 6))
                    draw_pos = (fruta_pantalla.x - 3, fruta_pantalla.y - 3 + float_y)
                    pantalla.blit(sprite_scaled, draw_pos)
                else:
                    pygame.draw.rect(pantalla, fruta.color, fruta_pantalla)

        if not self.invulnerable or int(pygame.time.get_ticks() / 100) % 2 == 0:
            jugador_pantalla = self.camera.aplicar(self.player.get_rect())
            sprite = self.player.get_current_sprite()
            if sprite:
                offset_x, offset_y = self.player.get_draw_offset()
                draw_pos = (jugador_pantalla.x - offset_x, jugador_pantalla.y - offset_y)
                pantalla.blit(sprite, draw_pos)
            else:
                color_jugador_actual = (0, 255, 0) if self.inmune else COLOR_JUGADOR
                pygame.draw.rect(pantalla, color_jugador_actual, jugador_pantalla)

        for monstruo in self.monstruos:
            monstruo_pantalla = self.camera.aplicar(monstruo.get_rect())
            sprite = monstruo.get_current_sprite()
            if sprite:
                offset_x, offset_y = monstruo.get_draw_offset()
                draw_pos = (monstruo_pantalla.x - offset_x, monstruo_pantalla.y - offset_y)
                pantalla.blit(sprite, draw_pos)
            else:
                pygame.draw.rect(pantalla, COLOR_MONSTRUO, monstruo_pantalla)

        self._dibujar_efecto_victoria(pantalla)
        dibujar_hud(pantalla, juego.vidas, juego.puntaje, self.tiempo_nivel, juego.nivel_actual, self.inmune)
