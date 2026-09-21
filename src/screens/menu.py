import pygame
from src.constants import COLOR_FONDO, COLOR_PANEL, COLOR_BORDE, COLOR_TEXTO, COLOR_TITULO, ANCHO_PANTALLA


class MenuScreen:
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.opcion_menu = (game.opcion_menu - 1) % len(game.opciones_menu)
            elif event.key == pygame.K_DOWN:
                game.opcion_menu = (game.opcion_menu + 1) % len(game.opciones_menu)
            elif event.key == pygame.K_RETURN:
                if game.opcion_menu == 0:
                    game.reiniciar_partida()
                    game.estado = game.estado_juego.JUEGO
                elif game.opcion_menu == 1:
                    pygame.quit()
                    import sys
                    sys.exit()

    def draw(self, game):
        pantalla = game.pantalla
        pantalla.fill(COLOR_FONDO)
        titulo = pygame.font.Font(None, 64).render("Maze Level One Game", True, COLOR_TITULO)
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 120))

        fuente = pygame.font.Font(None, 36)
        for i, opcion in enumerate(game.opciones_menu):
            color = COLOR_TITULO if i == game.opcion_menu else COLOR_TEXTO
            texto = fuente.render(opcion, True, color)
            pantalla.blit(texto, (ANCHO_PANTALLA // 2 - texto.get_width() // 2, 250 + i * 60))

        pygame.draw.rect(
            pantalla,
            COLOR_PANEL,
            (ANCHO_PANTALLA // 2 - 200, 230 + game.opcion_menu * 60, 400, 40),
            2,
        )
        pygame.display.flip()
