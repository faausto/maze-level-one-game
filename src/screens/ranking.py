import pygame
from src.constants import (
    ANCHO_PANTALLA,
    COLOR_BORDE_DORADO,
    COLOR_DORADO,
    COLOR_DORADO_CLARO,
    COLOR_PANEL_CREMA,
    COLOR_TEXTO_OSCURO,
)
from src.ui import fonts
from src.ui.background import dibujar_fondo_general
from src.ui.common import dibujar_panel, dibujar_separador, render_con_borde


class RankingScreen:
    def handle_event(self, game, event):
        if event.type != pygame.KEYDOWN:
            return

        if game.estado == game.estado_juego.RANKING_VICTORIA:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_ESCAPE):
                game.estado = game.estado_juego.FINAL
                game.opcion_menu = 0
        elif event.key == pygame.K_ESCAPE:
            game.estado = game.estado_juego.MENU

    def draw(self, game):
        pantalla = game.pantalla
        dibujar_fondo_general(pantalla, oscurecer=85)

        titulo = render_con_borde(fonts.fuente_titulo_pantalla, "Top 10", COLOR_DORADO)
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 56))
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            56 + titulo.get_height() + 8,
            280,
            COLOR_DORADO,
        )

        panel = pygame.Rect(142, 168, 740, 512)
        dibujar_panel(
            pantalla,
            panel,
            (*COLOR_PANEL_CREMA, 235),
            COLOR_BORDE_DORADO,
            3,
            18,
            COLOR_DORADO_CLARO,
            sombra=8,
        )

        x_rank = panel.x + 55
        x_name = panel.x + 140
        x_score_right = panel.right - 50
        y_header = panel.y + 24
        color_cabecera = (95, 75, 35)

        cabecera_rank = fonts.fuente_texto_pantalla_negrita.render(
            "Pos.", True, color_cabecera
        )
        cabecera_nombre = fonts.fuente_texto_pantalla_negrita.render(
            "Jugador", True, color_cabecera
        )
        cabecera_puntos = fonts.fuente_texto_pantalla_negrita.render(
            "Puntos", True, color_cabecera
        )
        pantalla.blit(cabecera_rank, (x_rank, y_header))
        pantalla.blit(cabecera_nombre, (x_name, y_header))
        pantalla.blit(
            cabecera_puntos, (x_score_right - cabecera_puntos.get_width(), y_header)
        )

        separador_y = panel.y + 62
        pygame.draw.line(
            pantalla,
            COLOR_BORDE_DORADO,
            (panel.x + 30, separador_y),
            (panel.right - 30, separador_y),
            2,
        )

        ranking = game.database.ranking
        if not ranking:
            texto = fonts.fuente_texto_pantalla.render(
                "No hay puntuaciones registradas", True, COLOR_TEXTO_OSCURO
            )
            pantalla.blit(
                texto,
                (panel.centerx - texto.get_width() // 2, panel.y + 220),
            )
        else:
            for i, entrada in enumerate(ranking[:10]):
                y = separador_y + 18 + i * 40
                if i % 2 == 0:
                    fila = pygame.Rect(panel.x + 20, y - 4, panel.width - 40, 34)
                    capa = pygame.Surface(fila.size, pygame.SRCALPHA)
                    pygame.draw.rect(
                        capa,
                        (205, 192, 160, 120),
                        capa.get_rect(),
                        border_radius=8,
                    )
                    pantalla.blit(capa, fila.topleft)

                color = (125, 88, 28) if i < 3 else COLOR_TEXTO_OSCURO
                rank = fonts.fuente_texto_pantalla_negrita.render(
                    f"{i + 1}.", True, color
                )
                nombre = fonts.fuente_texto_pantalla.render(
                    str(entrada["nombre"]), True, color
                )
                puntos = fonts.fuente_texto_pantalla.render(
                    str(entrada["puntaje"]), True, color
                )
                pantalla.blit(rank, (x_rank, y))
                pantalla.blit(nombre, (x_name, y))
                pantalla.blit(puntos, (x_score_right - puntos.get_width(), y))

        texto_opcion = render_con_borde(
            fonts.fuente_texto_pantalla_pequena,
            "Presiona ENTER para continuar"
            if game.estado == game.estado_juego.RANKING_VICTORIA
            else "Presiona ESC para volver",
            COLOR_DORADO_CLARO,
            grosor=1,
        )
        pantalla.blit(
            texto_opcion,
            (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 706),
        )
