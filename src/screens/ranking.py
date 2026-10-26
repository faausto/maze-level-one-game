import pygame
from src.constants import COLOR_FONDO, COLOR_TEXTO, COLOR_TITULO, ANCHO_PANTALLA
from src.ui import fonts


class RankingScreen:
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game.estado = game.estado_juego.MENU

    def draw(self, game):
        pantalla = game.pantalla
        pantalla.fill(COLOR_FONDO)
        titulo = fonts.fuente_titulo.render("Top 10", True, COLOR_TITULO)
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 60))

        ranking = game.database.ranking
        if not ranking:
            texto = fonts.fuente.render("No hay puntuaciones registradas", True, COLOR_TEXTO)
            pantalla.blit(texto, (ANCHO_PANTALLA // 2 - texto.get_width() // 2, 200))
        else:
            for i, entrada in enumerate(ranking[:10]):
                texto = fonts.fuente.render(f"{i+1}. {entrada['nombre']} - {entrada['puntaje']}", True, COLOR_TEXTO)
                pantalla.blit(texto, (ANCHO_PANTALLA // 2 - texto.get_width() // 2, 160 + i * 40))

        texto_opcion = fonts.fuente_pequena.render("Presiona ESC para volver", True, COLOR_TEXTO)
        pantalla.blit(texto_opcion, (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 550))
        pygame.display.flip()
