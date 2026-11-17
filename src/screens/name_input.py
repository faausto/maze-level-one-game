import pygame
from src.constants import (
    ANCHO_PANTALLA,
    COLOR_DORADO,
    COLOR_DORADO_CLARO,
    COLOR_FONDO,
    COLOR_PANEL_OSCURO,
    COLOR_TEXTO,
)
from src.ui import fonts
from src.ui.common import dibujar_panel, dibujar_separador, render_con_borde


class NameInputScreen:
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game.texto_nombre.strip():
                    game.database.guardar_puntaje(game.texto_nombre.strip(), game.puntaje_final)
                    game.cargar_ranking()
                    game.estado = game.estado_juego.RANKING_VICTORIA
                    game.opcion_menu = 0
            elif event.key == pygame.K_BACKSPACE:
                game.texto_nombre = game.texto_nombre[:-1]
            elif event.key == pygame.K_ESCAPE:
                game.estado = game.estado_juego.FINAL
                game.opcion_menu = 0
            else:
                if len(game.texto_nombre) < 15 and event.unicode.isprintable():
                    game.texto_nombre += event.unicode

    def draw(self, game):
        pantalla = game.pantalla
        pantalla.fill(COLOR_FONDO)

        titulo = render_con_borde(
            fonts.fuente_titulo_pantalla, "Victoria!", COLOR_DORADO
        )
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 130))
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            130 + titulo.get_height() + 8,
            300,
            COLOR_DORADO,
        )

        texto_puntaje = render_con_borde(
            fonts.fuente_puntaje_final,
            f"Puntaje final: {game.puntaje_final}",
            COLOR_DORADO_CLARO,
            grosor=2,
        )
        ancho_puntaje = max(420, texto_puntaje.get_width() + 64)
        panel_puntaje = pygame.Rect(
            ANCHO_PANTALLA // 2 - ancho_puntaje // 2, 236, ancho_puntaje, 72
        )
        dibujar_panel(
            pantalla,
            panel_puntaje,
            (*COLOR_PANEL_OSCURO, 180),
            COLOR_DORADO,
            2,
            16,
            COLOR_DORADO_CLARO,
            sombra=6,
        )
        pantalla.blit(
            texto_puntaje,
            (
                panel_puntaje.centerx - texto_puntaje.get_width() // 2,
                panel_puntaje.centery - texto_puntaje.get_height() // 2,
            ),
        )

        texto = render_con_borde(
            fonts.fuente_texto_pantalla,
            "Ingresa tu nombre:",
            COLOR_TEXTO,
            grosor=1,
        )
        pantalla.blit(
            texto, (ANCHO_PANTALLA // 2 - texto.get_width() // 2, 340)
        )

        input_rect = pygame.Rect(ANCHO_PANTALLA // 2 - 200, 388, 400, 64)
        dibujar_panel(
            pantalla,
            input_rect,
            (*COLOR_PANEL_OSCURO, 170),
            COLOR_DORADO,
            2,
            12,
            COLOR_DORADO_CLARO,
        )
        texto_nombre = fonts.fuente_texto_pantalla.render(
            game.texto_nombre or "_", True, COLOR_TEXTO
        )
        pantalla.blit(texto_nombre, (input_rect.x + 16, input_rect.y + 16))

        texto_opcion = render_con_borde(
            fonts.fuente_texto_pantalla_pequena,
            "Presiona ENTER para guardar",
            COLOR_DORADO_CLARO,
            grosor=1,
        )
        pantalla.blit(
            texto_opcion,
            (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 496),
        )
