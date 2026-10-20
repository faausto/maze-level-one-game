import pygame

class Laberinto:
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.mapa = [
            "1111111111111111111111",
            "1000000000100000000001",
            "1011111010101111111101",
            "1010001010100000001001",
            "1010101011111110101001",
            "1000101000000010101001",
            "1110101110111010101101",
            "1000100010001000100001",
            "1011111011101111101101",
            "1000001000100000001001",
            "1111101110101111111011",
            "1000001010100000001001",
            "1011111010111111101101",
            "1000000010000000000001",
            "1111111111111111111111",
        ]
        self.paredes = []
        self._construir_laberinto()
        
        # dimensiones del mundo
        self.ancho_mundo = len(self.mapa[0]) * self.tile_size
        self.alto_mundo = len(self.mapa) * self.tile_size

    def _construir_laberinto(self):
        for fila, texto in enumerate(self.mapa):
            for col, celda in enumerate(texto):
                if celda == "1":
                    self.paredes.append(
                        pygame.Rect(col * self.tile_size, fila * self.tile_size, self.tile_size, self.tile_size)
                    )

    def dibujar(self, pantalla, camara):
        for p in self.paredes:
            # ajustamos la posicion de las paredes
            r_proyectado = camara.aplicar_rect(p)
            pygame.draw.rect(pantalla, (70, 110, 200), r_proyectado)
