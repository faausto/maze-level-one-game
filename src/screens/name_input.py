import pygame
from src.constants import COLOR_FONDO, COLOR_PANEL, COLOR_TEXTO, COLOR_TITULO, ANCHO_PANTALLA
from src.ui import fonts


class NameInputScreen:
    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game.texto_nombre.strip():
                    game.database.guardar_puntaje(game.texto_nombre.strip(), game.puntaje_final)
                    game.cargar_ranking()
                    game.estado = game.estado_juego.FINAL
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
        titulo = fonts.fuente_titulo.render("Victoria!", True, COLOR_TITULO)
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 120))

        texto = fonts.fuente.render("Ingresa tu nombre:", True, COLOR_TEXTO)
        pantalla.blit(texto, (ANCHO_PANTALLA // 2 - texto.get_width() // 2, 220))

        input_rect = pygame.Rect(ANCHO_PANTALLA // 2 - 150, 280, 300, 50)
        pygame.draw.rect(pantalla, COLOR_PANEL, input_rect, 2)
        texto_nombre = fonts.fuente.render(game.texto_nombre or "_", True, COLOR_TEXTO)
        pantalla.blit(texto_nombre, (input_rect.x + 10, input_rect.y + 10))

        texto_opcion = fonts.fuente_pequena.render("Presiona ENTER para guardar", True, COLOR_TEXTO)
        pantalla.blit(texto_opcion, (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 360))
        pygame.display.flip()
