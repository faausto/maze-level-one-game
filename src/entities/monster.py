import pygame
import random
import os


class Monster:
    _sprite_sheet = None
    _animations = {}
    _frame_size = 128
    _cols = 6
    _rows = 4

    def __init__(self, x, y, ancho, alto, puntos, velocidad, rango_deteccion=0):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.puntos = puntos
        self.indice_punto = 0
        self.direccion = 1
        self.velocidad = velocidad
        self.rango_deteccion = rango_deteccion
        self.persiguiendo = False
        self.objetivo_wander = None
        self.origen_wander = (x, y)
        self.distancia_recorrida = 0
        self.max_distancia = random.randint(80, 160)
        self.tiempo_espera = 0
        self.viendo_hacia_atras = False
        self.visual_scale = 3.0
        self.visual_ancho = int(ancho * self.visual_scale)
        self.visual_alto = int(alto * self.visual_scale)
        self.dir_actual = 'abajo'
        self.frame_index = 0
        self.frame_time = 0.12
        self.frame_timer = 0.0
        self.is_moving = False
        self.last_dx = 0
        self.last_dy = 0

        if Monster._sprite_sheet is None:
            self._load_sprites()

    @classmethod
    def _load_sprites(cls):
        try:
            base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'images', 'monsters', 'witch.png')
            cls._sprite_sheet = pygame.image.load(base_path).convert_alpha()
            cls._animations = {
                'abajo': [],
                'izquierda': [],
                'derecha': [],
                'arriba': []
            }
            row_map = {
                0: 'abajo',
                1: 'izquierda',
                2: 'derecha',
                3: 'arriba'
            }
            for row in range(cls._rows):
                dir_name = row_map.get(row, 'abajo')
                for col in range(cls._cols):
                    x = col * cls._frame_size
                    y = row * cls._frame_size
                    frame = cls._sprite_sheet.subsurface(pygame.Rect(x, y, cls._frame_size, cls._frame_size))
                    cls._animations[dir_name].append(frame)
        except Exception as e:
            print(f"Error al cargar sprites del monstruo: {e}")
            cls._animations = {'abajo': [], 'izquierda': [], 'derecha': [], 'arriba': []}

    def _actualizar_direccion(self, dx, dy):
        if dx == 0 and dy == 0:
            return
        if abs(dx) > abs(dy):
            if dx > 0:
                self.dir_actual = 'derecha'
            else:
                self.dir_actual = 'izquierda'
        else:
            if dy > 0:
                self.dir_actual = 'abajo'
            else:
                self.dir_actual = 'arriba'

    def get_current_sprite(self):
        frames = Monster._animations.get(self.dir_actual, [])
        if frames:
            return pygame.transform.scale(frames[self.frame_index % len(frames)], (self.visual_ancho, self.visual_alto))
        return None

    def get_draw_offset(self):
        offset_x = (self.visual_ancho - self.rect.width) // 2
        offset_y = (self.visual_alto - self.rect.height) // 2
        return offset_x, offset_y - 10

    def _obtener_celda(self, maze, pos_x, pos_y):
        if not maze:
            return None
        tile_size = maze.tile_size
        cx = int(pos_x // tile_size)
        cy = int(pos_y // tile_size)
        if cy < 0 or cy >= len(maze.mapa) or cx < 0 or cx >= len(maze.mapa[0]):
            return None
        return maze.mapa[cy][cx]

    def _es_celda_valida(self, maze, x, y):
        if not maze:
            return True
        tile_size = maze.tile_size
        cx = int(x // tile_size)
        cy = int(y // tile_size)
        if cy < 0 or cy >= len(maze.mapa) or cx < 0 or cx >= len(maze.mapa[0]):
            return False
        if maze.mapa[cy][cx] == "1":
            return False
        test_rect = pygame.Rect(int(x), int(y), self.rect.width, self.rect.height)
        return not maze.colisiona(test_rect)

    def _generar_objetivo_wander(self, maze):
        if not maze:
            return
        tile_size = maze.tile_size
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(direcciones)
        for dx_dir, dy_dir in direcciones:
            dist_candidata = random.randint(60, self.max_distancia)
            nx = self.rect.x + dx_dir * dist_candidata
            ny = self.rect.y + dy_dir * dist_candidata
            if self._es_celda_valida(maze, nx, ny):
                self.objetivo_wander = (nx, ny)
                self.origen_wander = (self.rect.x, self.rect.y)
                self.distancia_recorrida = 0
                return
        self.objetivo_wander = (self.origen_wander[0], self.origen_wander[1])

    def update(self, dt, jugador_rect, maze=None, mundo_rect=None):
        if self.tiempo_espera > 0:
            self.tiempo_espera -= dt
            self.frame_timer += dt
            if self.frame_timer >= self.frame_time:
                self.frame_timer -= self.frame_time
                self.frame_index += 1
            return

        moved = False
        prev_x = self.rect.x
        prev_y = self.rect.y

        if self.rango_deteccion > 0 and jugador_rect and maze:
            dist_jugador = (
                (jugador_rect.centerx - self.rect.centerx) ** 2
                + (jugador_rect.centery - self.rect.centery) ** 2
            ) ** 0.5
            self.persiguiendo = dist_jugador <= self.rango_deteccion

        if self.persiguiendo and jugador_rect and maze:
            objetivo_x = jugador_rect.centerx - self.rect.width // 2
            objetivo_y = jugador_rect.centery - self.rect.height // 2
            dx_m = objetivo_x - self.rect.x
            dy_m = objetivo_y - self.rect.y
            dist_m = (dx_m ** 2 + dy_m ** 2) ** 0.5
            if dist_m > 0:
                angulo = pygame.math.Vector2(dx_m, dy_m).normalize()
                mov_x = angulo.x * self.velocidad * dt
                mov_y = angulo.y * self.velocidad * dt
                self._actualizar_direccion(mov_x, mov_y)
                if maze:
                    nuevo_rect_x = self.rect.move(mov_x, 0)
                    if not maze.colisiona(nuevo_rect_x):
                        self.rect.x = nuevo_rect_x.x
                        moved = moved or (self.rect.x != prev_x)
                    else:
                        self.persiguiendo = False
                        self.tiempo_espera = 0.2
                    nuevo_rect_y = self.rect.move(0, mov_y)
                    if not maze.colisiona(nuevo_rect_y):
                        self.rect.y = nuevo_rect_y.y
                        moved = moved or (self.rect.y != prev_y)
                    else:
                        self.persiguiendo = False
                        self.tiempo_espera = 0.2
                else:
                    self.rect.x += mov_x
                    self.rect.y += mov_y
                    moved = True
                if mundo_rect:
                    self.rect.clamp_ip(mundo_rect)
            self.is_moving = moved or dist_m > 0.1
        elif maze is None or self.objetivo_wander is None:
            if self.puntos and maze:
                objetivo = self.puntos[self.indice_punto]
                objetivo_x = objetivo[0]
                objetivo_y = objetivo[1]
                dx_m = objetivo_x - self.rect.x
                dy_m = objetivo_y - self.rect.y
                dist_m = (dx_m ** 2 + dy_m ** 2) ** 0.5
                if dist_m < max(2, self.velocidad * dt):
                    self.rect.x = objetivo_x
                    self.rect.y = objetivo_y
                    self.indice_punto = (self.indice_punto + self.direccion) % len(self.puntos)
                    self.is_moving = False
                    self.frame_timer += dt
                    if self.frame_timer >= self.frame_time:
                        self.frame_timer -= self.frame_time
                        self.frame_index += 1
                    return
                if dist_m > 0:
                    angulo = pygame.math.Vector2(dx_m, dy_m).normalize()
                    mov_x = angulo.x * self.velocidad * dt
                    mov_y = angulo.y * self.velocidad * dt
                    self._actualizar_direccion(mov_x, mov_y)
                    nuevo_rect_x = self.rect.move(mov_x, 0)
                    if not maze.colisiona(nuevo_rect_x):
                        self.rect.x = nuevo_rect_x.x
                    nuevo_rect_y = self.rect.move(0, mov_y)
                    if not maze.colisiona(nuevo_rect_y):
                        self.rect.y = nuevo_rect_y.y
                    if mundo_rect:
                        self.rect.clamp_ip(mundo_rect)
                    self.is_moving = True
                else:
                    self.is_moving = False
            else:
                self.is_moving = False
        else:
            objetivo_x, objetivo_y = self.objetivo_wander
            dx_m = objetivo_x - self.rect.x
            dy_m = objetivo_y - self.rect.y
            dist_m = (dx_m ** 2 + dy_m ** 2) ** 0.5

            if dist_m < 4:
                if (objetivo_x, objetivo_y) == (self.origen_wander[0], self.origen_wander[1]):
                    self._generar_objetivo_wander(maze)
                    self.max_distancia = random.randint(80, 160)
                else:
                    self.objetivo_wander = (self.origen_wander[0], self.origen_wander[1])
                self.is_moving = False
                self.frame_timer += dt
                if self.frame_timer >= self.frame_time:
                    self.frame_timer -= self.frame_time
                    self.frame_index += 1
                return

            if dist_m > 0:
                angulo = pygame.math.Vector2(dx_m, dy_m).normalize()
                mov_x = angulo.x * self.velocidad * dt
                mov_y = angulo.y * self.velocidad * dt
                self._actualizar_direccion(mov_x, mov_y)
                if maze:
                    nuevo_rect_x = self.rect.move(mov_x, 0)
                    if not maze.colisiona(nuevo_rect_x):
                        self.rect.x = nuevo_rect_x.x
                        moved = True
                    else:
                        self.objetivo_wander = (self.origen_wander[0], self.origen_wander[1])
                        self.is_moving = False
                        self.frame_timer += dt
                        if self.frame_timer >= self.frame_time:
                            self.frame_timer -= self.frame_time
                            self.frame_index += 1
                        return
                    nuevo_rect_y = self.rect.move(0, mov_y)
                    if not maze.colisiona(nuevo_rect_y):
                        self.rect.y = nuevo_rect_y.y
                        moved = True
                    else:
                        self.objetivo_wander = (self.origen_wander[0], self.origen_wander[1])
                        self.is_moving = False
                        self.frame_timer += dt
                        if self.frame_timer >= self.frame_time:
                            self.frame_timer -= self.frame_time
                            self.frame_index += 1
                        return
                    if mundo_rect:
                        self.rect.clamp_ip(mundo_rect)
                else:
                    self.rect.x += mov_x
                    self.rect.y += mov_y
                    moved = True
                    if mundo_rect:
                        self.rect.clamp_ip(mundo_rect)
                self.is_moving = True
            else:
                self.is_moving = False

        self.frame_timer += dt
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.frame_index += 1

    def get_rect(self):
        return self.rect
