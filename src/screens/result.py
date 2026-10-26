import pygame
from src.constants import COLOR_FONDO, COLOR_TEXTO, COLOR_TITULO, ANCHO_PANTALLA
from src.ui import fonts


class ResultScreen:
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game.estado = game.estado_juego.FINAL
            game.opcion_menu = 0

    def draw(self, game):
        pantalla = game.pantalla
        pantalla.fill(COLOR_FONDO)
        titulo = fonts.fuente_titulo.render(game.mensaje_resultado, True, COLOR_TITULO)
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 150))

        texto_puntaje = fonts.fuente.render(f"Puntaje final: {game.puntaje_final}", True, COLOR_TEXTO)
        pantalla.blit(texto_puntaje, (ANCHO_PANTALLA // 2 - texto_puntaje.get_width() // 2, 250))

        texto_opcion = fonts.fuente_pequena.render("Presiona ENTER para continuar", True, COLOR_TEXTO)
        pantalla.blit(texto_opcion, (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 350))
        pygame.display.flip()
