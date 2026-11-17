import pygame


def render_con_borde(fuente, texto, color, color_borde=(10, 12, 8), grosor=2):
    relleno = fuente.render(texto, True, color)
    borde = fuente.render(texto, True, color_borde)
    ancho = relleno.get_width() + grosor * 2
    alto = relleno.get_height() + grosor * 2
    superficie = pygame.Surface((ancho, alto), pygame.SRCALPHA)

    for dx in range(-grosor, grosor + 1):
        for dy in range(-grosor, grosor + 1):
            if dx * dx + dy * dy <= grosor * grosor:
                superficie.blit(borde, (grosor + dx, grosor + dy))
    superficie.blit(relleno, (grosor, grosor))
    return superficie


def dibujar_panel(
    pantalla,
    rect,
    relleno,
    borde,
    grosor=2,
    radio=16,
    borde_interno=None,
    sombra=0,
):
    if sombra:
        capa_sombra = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            capa_sombra, (0, 0, 0, 85), capa_sombra.get_rect(), border_radius=radio
        )
        pantalla.blit(capa_sombra, (rect.x + sombra, rect.y + sombra))

    capa = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(capa, relleno, capa.get_rect(), border_radius=radio)
    pantalla.blit(capa, rect.topleft)
    pygame.draw.rect(pantalla, borde, rect, grosor, border_radius=radio)

    if borde_interno:
        interior = rect.inflate(-10, -10)
        pygame.draw.rect(
            pantalla,
            borde_interno,
            interior,
            1,
            border_radius=max(1, radio - 5),
        )


def dibujar_separador(pantalla, centro_x, y, ancho, color):
    pygame.draw.line(
        pantalla,
        color,
        (centro_x - ancho // 2, y),
        (centro_x + ancho // 2, y),
        2,
    )
    pygame.draw.circle(pantalla, color, (centro_x - ancho // 2, y), 3)
    pygame.draw.circle(pantalla, color, (centro_x + ancho // 2, y), 3)
