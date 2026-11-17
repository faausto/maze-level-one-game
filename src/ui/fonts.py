import pygame

fuente = None
fuente_pequena = None
fuente_menu = None
fuente_titulo_pantalla = None
fuente_titulo_derrota = None
fuente_puntaje_final = None
fuente_texto_pantalla = None
fuente_texto_pantalla_pequena = None
fuente_texto_pantalla_negrita = None
fuente_hud_etiqueta = None
fuente_hud_valor = None

_FUENTES_SERIF = ("georgia", "palatinolinotype", "timesnewroman", "cambria")


def _crear_fuente_serif(tamano, negrita=False):
    for nombre in _FUENTES_SERIF:
        ruta = pygame.font.match_font(nombre, bold=negrita) or pygame.font.match_font(nombre)
        if ruta:
            fuente_serif = pygame.font.Font(ruta, tamano)
            fuente_serif.set_bold(negrita)
            return fuente_serif
    return pygame.font.Font(None, tamano)


def inicializar_fuentes():
    global fuente, fuente_pequena
    global fuente_menu, fuente_titulo_pantalla, fuente_titulo_derrota
    global fuente_puntaje_final
    global fuente_texto_pantalla, fuente_texto_pantalla_pequena
    global fuente_texto_pantalla_negrita
    global fuente_hud_etiqueta, fuente_hud_valor

    fuente = pygame.font.Font(None, 46)
    fuente_pequena = pygame.font.Font(None, 36)
    fuente_menu = _crear_fuente_serif(40, negrita=True)
    fuente_titulo_pantalla = _crear_fuente_serif(64, negrita=True)
    fuente_titulo_derrota = _crear_fuente_serif(110, negrita=True)
    fuente_puntaje_final = _crear_fuente_serif(42, negrita=True)
    fuente_texto_pantalla = _crear_fuente_serif(28)
    fuente_texto_pantalla_pequena = _crear_fuente_serif(24)
    fuente_texto_pantalla_negrita = _crear_fuente_serif(24, negrita=True)
    fuente_hud_etiqueta = _crear_fuente_serif(21, negrita=True)
    fuente_hud_valor = _crear_fuente_serif(36, negrita=True)
