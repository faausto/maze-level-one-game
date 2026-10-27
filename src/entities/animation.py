import pygame
import os


class SpriteSheet:
    def __init__(self, image_path, frame_width, frame_height, cols, rows, total_frames=None):
        self.image_path = image_path
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.cols = cols
        self.rows = rows
        self.total_frames = total_frames
        self.sheet = None
        self.frames = None
        self._loaded = False

    def _ensure_loaded(self):
        if not self._loaded:
            self.sheet = pygame.image.load(self.image_path).convert_alpha()
            self.frames = self._extract_frames()
            self._loaded = True

    def _extract_frames(self):
        frames = []
        count = 0
        max_frames = self.total_frames if self.total_frames else self.cols * self.rows
        for row in range(self.rows):
            for col in range(self.cols):
                if count >= max_frames:
                    break
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                frames.append(frame)
                count += 1
            if count >= max_frames:
                break
        return frames

    def get_frame(self, index):
        self._ensure_loaded()
        if 0 <= index < len(self.frames):
            return self.frames[index]
        return self.frames[0]

    def get_frame_count(self):
        self._ensure_loaded()
        return len(self.frames)


class Animation:
    def __init__(self, sprite_sheet, fps=12, loop=True):
        self.sprite_sheet = sprite_sheet
        self.fps = fps
        self.frame_time = 1.0 / fps
        self.current_frame = 0
        self.elapsed_time = 0.0
        self.is_playing = True
        self.loop = loop
        self.finished = False

    def update(self, dt):
        if not self.is_playing or self.finished:
            return
        self.elapsed_time += dt
        if self.elapsed_time >= self.frame_time:
            self.elapsed_time -= self.frame_time
            self.current_frame += 1
            if self.current_frame >= self.sprite_sheet.get_frame_count():
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = self.sprite_sheet.get_frame_count() - 1
                    self.finished = True

    def get_current_frame(self):
        return self.sprite_sheet.get_frame(self.current_frame)

    def reset(self):
        self.current_frame = 0
        self.elapsed_time = 0.0
        self.finished = False

    def set_fps(self, fps):
        self.fps = fps
        self.frame_time = 1.0 / fps


class DirectionalAnimation:
    DIRECTIONS = [
        'norte', 'sur', 'este', 'oeste',
        'noreste', 'noroeste', 'sureste', 'suroeste'
    ]

    def __init__(self, base_path, prefix, frame_width, frame_height, cols, rows, fps=12, loop=True, total_frames=None):
        self.animations = {}
        self.current_direction = 'sur'
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.cols = cols
        self.rows = rows
        self.fps = fps
        self.loop = loop
        self.total_frames = total_frames
        self.base_path = base_path
        self.prefix = prefix
        self._initialized = False

    def _ensure_initialized(self):
        if not self._initialized:
            for direction in self.DIRECTIONS:
                path = os.path.join(self.base_path, f'{self.prefix}_{direction}.png')
                if os.path.exists(path):
                    sheet = SpriteSheet(path, self.frame_width, self.frame_height, self.cols, self.rows, self.total_frames)
                    self.animations[direction] = Animation(sheet, self.fps, self.loop)
                else:
                    print(f"Advertencia: No se encontró {path}")
            self._initialized = True

    def set_direction(self, direction):
        self._ensure_initialized()
        if direction in self.animations and direction != self.current_direction:
            self.current_direction = direction
            self.animations[direction].reset()

    def update(self, dt):
        self._ensure_initialized()
        if self.current_direction in self.animations:
            self.animations[self.current_direction].update(dt)

    def get_current_frame(self):
        self._ensure_initialized()
        if self.current_direction in self.animations:
            return self.animations[self.current_direction].get_current_frame()
        return None

    def get_direction_from_vector(self, dx, dy):
        if dx == 0 and dy == 0:
            return self.current_direction

        if dx > 0 and dy < 0:
            return 'noreste'
        elif dx < 0 and dy < 0:
            return 'noroeste'
        elif dx > 0 and dy > 0:
            return 'sureste'
        elif dx < 0 and dy > 0:
            return 'suroeste'
        elif dx > 0:
            return 'este'
        elif dx < 0:
            return 'oeste'
        elif dy < 0:
            return 'norte'
        else:
            return 'sur'

    def is_finished(self):
        self._ensure_initialized()
        if self.current_direction in self.animations:
            return self.animations[self.current_direction].finished
        return False

    def reset(self):
        self._ensure_initialized()
        if self.current_direction in self.animations:
            self.animations[self.current_direction].reset()