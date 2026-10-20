import pygame
import os

def inicializar_audio():
    pygame.mixer.init()

def cargar_sonido(ruta):
    if os.path.exists(ruta):
        return pygame.mixer.Sound(ruta)
    return None

def cargar_musica(ruta):
    if os.path.exists(ruta):
        pygame.mixer.music.load(ruta)
        return True
    return False

def reproducir_musica(volumen=0.3, loops=-1):
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(loops)

def detener_musica():
    pygame.mixer.music.stop()