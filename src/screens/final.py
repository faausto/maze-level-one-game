import pygame
from src.constants import COLOR_FONDO, COLOR_PANEL, COLOR_BORDE, COLOR_TEXTO, COLOR_TITULO, ANCHO_PANTALLA
from src.ui import fonts
from src.ui.menu_ui import dibujar_opciones_menu


class FinalScreen:
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.opcion_menu = (game.opcion_menu - 1) % 2
            elif event.key == pygame.K_DOWN:
                game.opcion_menu = (game.opcion_menu + 1) % 2
            elif event.key == pygame.K_RETURN:
                if game.opcion_menu == 0:
                    game.reiniciar_partida()
                    game.estado = game.estado_juego.JUEGO
                else:
                    game.estado = game.estado_juego.MENU

    def draw(self, game):
        pantalla = game.pantalla
        pantalla.fill(COLOR_FONDO)
        titulo = fonts.fuente_titulo.render(game.mensaje_resultado, True, COLOR_TITULO)
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 100))

        texto_puntaje = fonts.fuente.render(f"Puntaje final: {game.puntaje_final}", True, COLOR_TEXTO)
        pantalla.blit(texto_puntaje, (ANCHO_PANTALLA // 2 - texto_puntaje.get_width() // 2, 180))

        opciones = ["Jugar de nuevo", "Volver al menu principal"]
        dibujar_opciones_menu(pantalla, opciones, game.opcion_menu)

        pygame.draw.rect(
            pantalla,
            COLOR_PANEL,
            (ANCHO_PANTALLA // 2 - 220, 290 + game.opcion_menu * 60, 440, 40),
            2,
        )
        pygame.display.flip()
