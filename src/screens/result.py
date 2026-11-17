import pygame
from src.constants import (
    ANCHO_PANTALLA,
    COLOR_BORDE_DERROTA,
    COLOR_DERROTA,
    COLOR_DERROTA_CLARO,
    COLOR_DORADO,
    COLOR_DORADO_CLARO,
    COLOR_FONDO,
    COLOR_PANEL_DERROTA,
    COLOR_TEXTO,
)
from src.ui import fonts
from src.ui.background import dibujar_fondo_gameover
from src.ui.common import dibujar_panel, dibujar_separador, render_con_borde


class ResultScreen:
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game.estado = game.estado_juego.FINAL
            game.opcion_menu = 0

    def draw(self, game):
        pantalla = game.pantalla
        es_victoria = "victoria" in game.mensaje_resultado.lower()

        if es_victoria:
            pantalla.fill(COLOR_FONDO)
            titulo = render_con_borde(
                fonts.fuente_titulo_pantalla,
                game.mensaje_resultado,
                COLOR_DORADO,
            )
            pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 192))
            dibujar_separador(
                pantalla,
                ANCHO_PANTALLA // 2,
                192 + titulo.get_height() + 8,
                300,
                COLOR_DORADO,
            )

            texto_puntaje = render_con_borde(
                fonts.fuente_texto_pantalla,
                f"Puntaje final: {game.puntaje_final}",
                COLOR_TEXTO,
                grosor=1,
            )
            pantalla.blit(
                texto_puntaje,
                (ANCHO_PANTALLA // 2 - texto_puntaje.get_width() // 2, 320),
            )

            texto_opcion = render_con_borde(
                fonts.fuente_texto_pantalla_pequena,
                "Presiona ENTER para continuar",
                COLOR_DORADO_CLARO,
                grosor=1,
            )
            pantalla.blit(
                texto_opcion,
                (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 448),
            )
            return

        dibujar_fondo_gameover(pantalla, oscurecer=120)

        panel = pygame.Rect(182, 150, 660, 430)
        dibujar_panel(
            pantalla,
            panel,
            (*COLOR_PANEL_DERROTA, 205),
            COLOR_DERROTA,
            2,
            20,
            COLOR_BORDE_DERROTA,
            sombra=10,
        )

        titulo = render_con_borde(
            fonts.fuente_titulo_derrota,
            "DERROTA",
            COLOR_DERROTA,
            (6, 3, 6),
            grosor=4,
        )
        y_titulo = panel.y + 24
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, y_titulo))
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            y_titulo + titulo.get_height() + 8,
            340,
            COLOR_BORDE_DERROTA,
        )

        subtitulo = render_con_borde(
            fonts.fuente_texto_pantalla,
            "La oscuridad te alcanzó en el laberinto...",
            COLOR_DERROTA_CLARO,
            grosor=1,
        )
        pantalla.blit(
            subtitulo,
            (ANCHO_PANTALLA // 2 - subtitulo.get_width() // 2, 400),
        )

        texto_puntaje = render_con_borde(
            fonts.fuente_texto_pantalla,
            f"Puntaje final: {game.puntaje_final}",
            COLOR_TEXTO,
            grosor=1,
        )
        pantalla.blit(
            texto_puntaje,
            (ANCHO_PANTALLA // 2 - texto_puntaje.get_width() // 2, 458),
        )

        texto_opcion = render_con_borde(
            fonts.fuente_texto_pantalla_pequena,
            "Presiona ENTER para continuar",
            COLOR_DERROTA_CLARO,
            grosor=1,
        )
        pantalla.blit(
            texto_opcion,
            (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 524),
        )
