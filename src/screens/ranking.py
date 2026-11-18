"""Pantalla de la tabla de puntuaciones (Top 10)."""

import pygame

from src.constants import (
    ANCHO_PANTALLA,
    COLOR_BORDE_DORADO,
    COLOR_DORADO,
    COLOR_DORADO_CLARO,
    COLOR_PANEL_CREMA,
    COLOR_TEXTO_OSCURO,
)
from src.estados import EstadoJuego
from src.ui import fonts
from src.ui.background import dibujar_fondo_general
from src.ui.common import dibujar_panel, dibujar_separador, render_con_borde


class RankingScreen:
    """Muestra el Top 10 del ranking y permite continuar."""

    def handle_event(self, game, event):
        """Devuelve el próximo estado según el modo de ranking, o None."""
        if event.type != pygame.KEYDOWN:
            return None

        if game.estado == EstadoJuego.RANKING_VICTORIA:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_ESCAPE):
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    game.audio.reproducir("menu_confirm")
                game.opcion_menu = 0
                return EstadoJuego.FINAL
        elif event.key == pygame.K_ESCAPE:
            return EstadoJuego.MENU
        return None

    def draw(self, game):
        """Dibuja el Top 10 con el nombre y el puntaje de cada jugador."""
        pantalla = game.pantalla
        dibujar_fondo_general(pantalla, oscurecer=85)

        self._dibujar_titulo(pantalla)
        panel = self._dibujar_panel(pantalla)
        separador_y = self._dibujar_cabecera(pantalla, panel)
        self._dibujar_ranking(
            pantalla, panel, game.database.ranking, separador_y
        )
        self._dibujar_ayuda(pantalla, game.estado)

    def _dibujar_titulo(self, pantalla):
        """Dibuja el título y su separador."""
        titulo = render_con_borde(
            fonts.fuente_titulo_pantalla, "Top 10", COLOR_DORADO
        )
        pantalla.blit(
            titulo, (ANCHO_PANTALLA // 2 - titulo.get_width() // 2, 56)
        )
        dibujar_separador(
            pantalla,
            ANCHO_PANTALLA // 2,
            56 + titulo.get_height() + 8,
            280,
            COLOR_DORADO,
        )

    def _dibujar_panel(self, pantalla):
        """Dibuja el panel del ranking y lo devuelve."""
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
        return panel

    def _dibujar_cabecera(self, pantalla, panel):
        """Dibuja la cabecera de la tabla y devuelve la línea divisoria."""
        color_cabecera = (95, 75, 35)
        x_rank = panel.x + 55
        x_name = panel.x + 140
        x_score_right = panel.right - 50
        y_header = panel.y + 24

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
            cabecera_puntos,
            (x_score_right - cabecera_puntos.get_width(), y_header),
        )

        separador_y = panel.y + 62
        pygame.draw.line(
            pantalla,
            COLOR_BORDE_DORADO,
            (panel.x + 30, separador_y),
            (panel.right - 30, separador_y),
            2,
        )
        return separador_y

    def _dibujar_ranking(self, pantalla, panel, ranking, separador_y):
        """Dibuja las filas del ranking o el aviso de tabla vacía."""
        if not ranking:
            self._dibujar_ranking_vacio(pantalla, panel)
            return
        for i, entrada in enumerate(ranking[:10]):
            self._dibujar_fila(pantalla, panel, entrada, i, separador_y)

    def _dibujar_ranking_vacio(self, pantalla, panel):
        """Dibuja el aviso cuando no hay puntuaciones."""
        texto = fonts.fuente_texto_pantalla.render(
            "No hay puntuaciones registradas", True, COLOR_TEXTO_OSCURO
        )
        pantalla.blit(
            texto,
            (panel.centerx - texto.get_width() // 2, panel.y + 220),
        )

    def _dibujar_fila(self, pantalla, panel, entrada, i, separador_y):
        """Dibuja una fila del ranking."""
        y = separador_y + 18 + i * 40
        if i % 2 == 0:
            self._dibujar_fondo_fila(pantalla, panel, y)

        color = (125, 88, 28) if i < 3 else COLOR_TEXTO_OSCURO
        x_rank = panel.x + 55
        x_name = panel.x + 140
        x_score_right = panel.right - 50
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

    def _dibujar_fondo_fila(self, pantalla, panel, y):
        """Dibuja la banda de fondo de las filas pares."""
        fila = pygame.Rect(panel.x + 20, y - 4, panel.width - 40, 34)
        capa = pygame.Surface(fila.size, pygame.SRCALPHA)
        pygame.draw.rect(
            capa, (205, 192, 160, 120), capa.get_rect(), border_radius=8
        )
        pantalla.blit(capa, fila.topleft)

    def _dibujar_ayuda(self, pantalla, estado):
        """Dibuja la ayuda de navegación adecuada al modo."""
        texto_opcion = render_con_borde(
            fonts.fuente_texto_pantalla_pequena,
            "Presiona ENTER para continuar"
            if estado == EstadoJuego.RANKING_VICTORIA
            else "Presiona ESC para volver",
            COLOR_DORADO_CLARO,
            grosor=1,
        )
        pantalla.blit(
            texto_opcion,
            (ANCHO_PANTALLA // 2 - texto_opcion.get_width() // 2, 706),
        )
