import pygame

fuente = None
fuente_pequena = None
fuente_titulo = None


def inicializar_fuentes():
    global fuente, fuente_pequena, fuente_titulo
    fuente = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 28)
    fuente_titulo = pygame.font.Font(None, 64)
