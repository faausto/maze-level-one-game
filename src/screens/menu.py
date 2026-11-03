import pygame
import os
from src.constants import COLOR_FONDO, COLOR_PANEL, COLOR_BORDE, COLOR_TEXTO, COLOR_TITULO, ANCHO_PANTALLA, ALTO_PANTALLA
from src.ui import fonts
from src.ui.menu_ui import dibujar_opciones_menu


class MenuScreen:
    _background = None

    def __init__(self):
        if MenuScreen._background is None:
            self._cargar_fondo()

    def _cargar_fondo(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            bg_path = os.path.join(base_dir, "assets", "images", "background", "menu_backbround.png")
            img = pygame.image.load(bg_path).convert()
            MenuScreen._background = pygame.transform.scale(img, (ANCHO_PANTALLA, ALTO_PANTALLA))
        except Exception as e:
            print(f"Error cargando fondo del menu: {e}")
            MenuScreen._background = None

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
                    game.estado = game.estado_juego.INSTRUCCIONES
                elif game.opcion_menu == 2:
                    game.cargar_ranking()
                    game.estado = game.estado_juego.RANKING
                elif game.opcion_menu == 3:
                    pygame.quit()
                    import sys
                    sys.exit()

    def draw(self, game):
        pantalla = game.pantalla
        if MenuScreen._background:
            pantalla.blit(MenuScreen._background, (0, 0))
        else:
            pantalla.fill(COLOR_FONDO)
        titulo = fonts.fuente_titulo.render("Maze Level One Game", True, COLOR_TITULO)
        pantalla.blit(titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 120))

        dibujar_opciones_menu(pantalla, game.opciones_menu, game.opcion_menu)

        pygame.draw.rect(
            pantalla,
            COLOR_PANEL,
            (ANCHO_PANTALLA // 2 - 200, 230 + game.opcion_menu * 60, 400, 40),
            2,
        )
        pygame.display.flip()
