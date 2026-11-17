import os
import pygame

_DIRECTORIO_SONIDOS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets",
    "sounds",
)

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
    def __init__(self):
        self.disponible = False
        self.musica_actual = None
        self.canal_musica = None
        self.canal_pasos = None

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
        except pygame.error:
            return

        if pygame.mixer.get_init() is None:
            return

        pygame.mixer.set_num_channels(16)
        pygame.mixer.set_reserved(2)
        self.canal_musica = pygame.mixer.Channel(0)
        self.canal_pasos = pygame.mixer.Channel(1)
        self.disponible = True

    def _ruta_sonido(self, nombre):
        for extension in (".wav", ".ogg", ".mp3"):
            ruta = os.path.join(_DIRECTORIO_SONIDOS, nombre + extension)
            if os.path.exists(ruta):
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
                    sonido = pygame.mixer.Sound(ruta)
                    sonido.set_volume(_VOLUMENES.get(nombre, 0.5))
                except pygame.error as e:
                    print(f"Error cargando sonido {nombre}: {e}")

        _sonidos[nombre] = sonido
        return sonido

    def reproducir(self, nombre):
        if not self.disponible:
            return
        sonido = self._obtener(nombre)
        if sonido:
            sonido.play()

    def reproducir_paso(self):
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
        if not self.disponible or self.musica_actual == nombre:
            return

        self.musica_actual = nombre
        self.canal_musica.stop()
        sonido = self._obtener(nombre)
        if sonido:
            self.canal_musica.play(sonido, loops=-1, fade_ms=600)
