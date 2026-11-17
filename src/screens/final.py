import pygame
from src.constants import (
    ANCHO_PANTALLA,
    COLOR_BORDE_DERROTA,
    COLOR_DERROTA,
    COLOR_DERROTA_CLARO,
    COLOR_DORADO,
    COLOR_DORADO_CLARO,
    COLOR_PANEL_DERROTA,
    COLOR_PANEL_OSCURO,
    COLOR_TEXTO,
)
from src.ui import fonts
from src.ui.background import dibujar_fondo_gameover, dibujar_fondo_general
from src.ui.common import dibujar_panel, dibujar_separador, render_con_borde
from src.ui.menu_ui import dibujar_opciones_menu


class FinalScreen:
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.opcion_menu = (game.opcion_menu - 1) % 2
                game.audio.reproducir("menu_select")
            elif event.key == pygame.K_DOWN:
                game.opcion_menu = (game.opcion_menu + 1) % 2
                game.audio.reproducir("menu_select")
            elif event.key == pygame.K_RETURN:
                game.audio.reproducir("menu_confirm")
                if game.opcion_menu == 0:
                    game.reiniciar_partida()
                    game.estado = game.estado_juego.JUEGO
                else:
                    game.estado = game.estado_juego.MENU

    def draw(self, game):
        pantalla = game.pantalla
        es_victoria = "victoria" in game.mensaje_resultado.lower()

        if es_victoria:
            dibujar_fondo_general(pantalla, oscurecer=80)
            relleno_panel = (*COLOR_PANEL_OSCURO, 185)
            borde_panel = COLOR_DORADO
            borde_interno = COLOR_DORADO_CLARO
            color_titulo = COLOR_DORADO
            color_ayuda = COLOR_DORADO_CLARO
            texto_titulo = game.mensaje_resultado
            fuente_titulo = fonts.fuente_titulo_pantalla
            y_titulo = 100
        else:
            dibujar_fondo_gameover(pantalla, oscurecer=110)
            relleno_panel = (*COLOR_PANEL_DERROTA, 205)
            borde_panel = COLOR_DERROTA
            borde_interno = COLOR_BORDE_DERROTA
            color_titulo = COLOR_DERROTA
            color_ayuda = COLOR_DERROTA_CLARO
            texto_titulo = "DERROTA"
            fuente_titulo = fonts.fuente_titulo_derrota
            y_titulo = 82

        panel = pygame.Rect(192, 70, 640, 610)
        dibujar_panel(
            pantalla,
            panel,
            relleno_panel,
            borde_panel,
            2,
            20,
            borde_interno,
            sombra=8,
        )

        titulo = render_con_borde(
            fuente_titulo,
            texto_titulo,
            color_titulo,
            (6, 3, 6) if not es_victoria else (10, 12, 8),
            grosor=4 if not es_victoria else 2,
        )
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, y_titulo))
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            y_titulo + titulo.get_height() + 8,
            300,
            borde_interno if not es_victoria else color_titulo,
        )

        texto_puntaje = render_con_borde(
            fonts.fuente_puntaje_final,
            f"Puntaje final: {game.puntaje_final}",
            COLOR_DORADO_CLARO if es_victoria else COLOR_TEXTO,
            grosor=2,
        )
        pantalla.blit(
            texto_puntaje,
            (
                ANCHO_PANTALLA // 2 - texto_puntaje.get_width() // 2,
                240 if es_victoria else 250,
            ),
        )

        opciones = ["Jugar de nuevo", "Volver al menu principal"]
        dibujar_opciones_menu(pantalla, opciones, game.opcion_menu)

        texto_opcion = render_con_borde(
            fonts.fuente_texto_pantalla_pequena,
            "Usa las flechas y ENTER para elegir",
            color_ayuda,
            grosor=1,
        )
        pantalla.blit(
            texto_opcion,
            (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 610),
        )
