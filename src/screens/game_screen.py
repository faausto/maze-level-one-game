import pygame
import random
from src.constants import (
    COLOR_FONDO,
    COLOR_PARED,
    COLOR_BORDE_PARED,
    COLOR_CAMINO,
    COLOR_BORDE_CAMINO,
    COLOR_OBJETIVO,
    COLOR_SALIDA,
    COLOR_JUGADOR,
    COLOR_MONSTRUO,
    COLOR_TITULO,
    ANCHO_PANTALLA,
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

    def cargar_nivel(self, nivel, juego):
        self.maze = Maze(nivel)
        self.camera = Camera(self.maze.ancho, self.maze.alto, ANCHO_PANTALLA, 600)
        mundo_rect = pygame.Rect(0, 0, self.maze.ancho, self.maze.alto)
        posiciones = self.maze.obtener_posiciones_libres()

        spawn = posiciones[0] if posiciones else (50, 50)
        self.player = Player(spawn[0] - 20, spawn[1] - 20)

        objetivo_pos = posiciones[1] if len(posiciones) > 1 else (spawn[0] + 100, spawn[1])
        juego.objetivo = pygame.Rect(objetivo_pos[0] - 20, objetivo_pos[1] - 20, 40, 40)

        self.frutas = []
        for f in FRUTAS_POR_NIVEL[nivel]:
            self.frutas.append(Fruit(f["x"], f["y"], tipo=f["tipo"], color=f["color"], puntos=f["puntos"]))

        self.monstruos = []
        for m in MONSTRUOS_POR_NIVEL[nivel]:
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

        salida = SALIDAS[nivel]
        self.salida = pygame.Rect(salida["x"], salida["y"], salida["ancho"], salida["alto"])
        self.tiempo_nivel = NIVELES[nivel]["tiempo"]
        self.frutas_recolectadas_ventana = []
        self.inmune = False
        self.tiempo_inmunidad = 0
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 0

    def update(self, juego, dt):
        if juego.estado != juego.estado_juego.JUEGO:
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

        for fruta in self.frutas:
            if fruta.esta_activa() and self.player.get_rect().colliderect(fruta.get_rect()):
                fruta.recolectar()
                juego.puntaje += fruta.puntos
                ahora = pygame.time.get_ticks() / 1000.0
                self.frutas_recolectadas_ventana.append(ahora)
                self.frutas_recolectadas_ventana = [t for t in self.frutas_recolectadas_ventana if ahora - t <= 10]
                if len(self.frutas_recolectadas_ventana) >= 3:
                    self.inmune = True
                    self.tiempo_inmunidad = 5
                    self.frutas_recolectadas_ventana = []

        for monstruo in self.monstruos:
            monstruo.update(dt, self.player.get_rect())

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

        if self.player.get_rect().colliderect(self.salida):
            if juego.nivel_actual < len(NIVELES) - 1:
                juego.nivel_actual += 1
                self.cargar_nivel(juego.nivel_actual, juego)
            else:
                bonus = 100 + juego.vidas * 50 + int(self.tiempo_nivel) * 5
                juego.puntaje_final = juego.puntaje + bonus
                juego.mensaje_resultado = "Victoria"
                juego.estado = juego.estado_juego.INGRESO_NOMBRE

    def draw(self, juego):
        self.camera.update(self.player.get_rect())
        pantalla = juego.pantalla
        pantalla.fill(COLOR_FONDO)

        self.maze.dibujar(pantalla, self.camera)

        objetivo_pantalla = self.camera.aplicar(juego.objetivo)
        pygame.draw.rect(pantalla, COLOR_OBJETIVO, objetivo_pantalla)

        salida_pantalla = self.camera.aplicar(self.salida)
        pygame.draw.rect(pantalla, COLOR_SALIDA, salida_pantalla)

        for fruta in self.frutas:
            if fruta.esta_activa():
                fruta_pantalla = self.camera.aplicar(fruta.get_rect())
                pygame.draw.rect(pantalla, fruta.color, fruta_pantalla)

        if not self.invulnerable or int(pygame.time.get_ticks() / 100) % 2 == 0:
            jugador_pantalla = self.camera.aplicar(self.player.get_rect())
            color_jugador_actual = (0, 255, 0) if self.inmune else COLOR_JUGADOR
            pygame.draw.rect(pantalla, color_jugador_actual, jugador_pantalla)

        for monstruo in self.monstruos:
            monstruo_pantalla = self.camera.aplicar(monstruo.get_rect())
            pygame.draw.rect(pantalla, COLOR_MONSTRUO, monstruo_pantalla)

        dibujar_hud(pantalla, juego.vidas, juego.puntaje, self.tiempo_nivel, juego.nivel_actual, self.inmune)
        pygame.display.flip()
