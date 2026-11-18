"""Música de fondo y efectos de sonido del juego."""

import logging

import pygame

from src.constants import SOUNDS_DIR

logger = logging.getLogger(__name__)

_VOLUMENES = {
    "collect": 0.55,
    "damage": 0.65,
    "final_victory": 0.65,
    "game_over": 0.65,
    "inmune": 0.60,
    "maze_lv1": 0.18,
    "menu_sound": 0.22,
    "menu_confirm": 0.55,
    "menu_select": 0.40,
    "step": 0.28,
    "success_level": 0.65,
}

_sonidos = {}


class Audio:
    """Carga y reproduce la música y los efectos de sonido del juego."""

    def __init__(self):
        self.disponible = False
        self.musica_actual = None
        self.canal_pasos = None

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
        except pygame.error as error:
            logger.warning("Audio no disponible: %s", error)
            return

        if pygame.mixer.get_init() is None:
            return

        pygame.mixer.set_num_channels(16)
        pygame.mixer.set_reserved(1)
        self.canal_pasos = pygame.mixer.Channel(0)
        self.disponible = True

    def _ruta_sonido(self, nombre):
        for extension in (".wav", ".ogg", ".mp3"):
            ruta = SOUNDS_DIR / f"{nombre}{extension}"
            if ruta.exists():
                return ruta
        return None

    def _obtener(self, nombre):
        if nombre in _sonidos:
            return _sonidos[nombre]

        sonido = None
        if self.disponible:
            ruta = self._ruta_sonido(nombre)
            if ruta:
                try:
                    sonido = pygame.mixer.Sound(str(ruta))
                    sonido.set_volume(_VOLUMENES.get(nombre, 0.5))
                except pygame.error as error:
                    logger.warning("No se pudo cargar el sonido %s: %s", nombre, error)

        _sonidos[nombre] = sonido
        return sonido

    def reproducir(self, nombre):
        """Reproduce un efecto corto (cargado una sola vez en memoria)."""
        if not self.disponible:
            return
        sonido = self._obtener(nombre)
        if sonido:
            sonido.play()

    def reproducir_paso(self):
        """Reproduce el sonido de paso si el canal de pasos está libre."""
        if not self.disponible:
            return
        if self.canal_pasos.get_busy():
            return
        sonido = self._obtener("step")
        if sonido:
            self.canal_pasos.play(sonido)

    def detener_pasos(self):
        if self.canal_pasos:
            self.canal_pasos.stop()

    def reproducir_musica(self, nombre):
        """Reproduce la música en loop usando streaming desde el disco."""
        if not self.disponible or self.musica_actual == nombre:
            return

        ruta = self._ruta_sonido(nombre)
        if not ruta:
            logger.warning("No se encontró la música: %s", nombre)
            self.musica_actual = nombre
            return

        try:
            pygame.mixer.music.load(str(ruta))
            pygame.mixer.music.set_volume(_VOLUMENES.get(nombre, 0.5))
            pygame.mixer.music.play(loops=-1, fade_ms=600)
        except pygame.error as error:
            logger.warning("No se pudo reproducir la música %s: %s", nombre, error)

        self.musica_actual = nombre

    def detener_musica(self, fade_ms=500):
        """Detiene la música actual con un fundido de salida."""
        if not self.disponible:
            return
        pygame.mixer.music.fadeout(fade_ms)
        self.musica_actual = None
