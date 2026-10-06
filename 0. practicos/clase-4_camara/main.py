import pygame

# llamamos a las clases camara y laberinto
from laberinto import Laberinto
from camara import Camara

pygame.init()
TILE = 40
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto con cámara")
clock = pygame.time.Clock()

# instanciamos laberinto
laberinto = Laberinto(TILE)

# instanciamos camara, usamos dimensiones de pantalla y laberinto
camara = Camara(ANCHO, ALTO, laberinto.ancho_mundo, laberinto.alto_mundo)

# JUGADOR
jugador = pygame.Rect(TILE + 5, TILE + 5, 30, 30)
velocidad = 4

# META
meta = pygame.Rect(
    laberinto.ancho_mundo - TILE - 40,
    laberinto.alto_mundo - TILE - 40,
    TILE,
    TILE
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx = -velocidad
    if keys[pygame.K_RIGHT]:
        dx = velocidad
    if keys[pygame.K_UP]:
        dy = -velocidad
    if keys[pygame.K_DOWN]:
        dy = velocidad

    # colisiones en x
    jugador.x += dx
    for p in laberinto.paredes:
        if jugador.colliderect(p):
            if dx > 0:
                jugador.right = p.left
            elif dx < 0:
                jugador.left = p.right
                
    # colisiones en y
    jugador.y += dy
    for p in laberinto.paredes:
        if jugador.colliderect(p):
            if dy > 0:
                jugador.bottom = p.top
            elif dy < 0:
                jugador.top = p.bottom

    if jugador.colliderect(meta):
        print("¡Ganaste!")
        running = False
    
    # actualizar camara segun jugador
    camara.actualizar(jugador)

    pantalla.fill((20, 20, 30))
    
    # dibujar laberinto
    laberinto.dibujar(pantalla, camara)

    # dibujar jugador segun camara
    r_jug = camara.aplicar_rect(jugador)
    pygame.draw.rect(pantalla, (240, 200, 80), r_jug)

    # dibujar la meta
    r_meta = camara.aplicar_rect(meta)
    pygame.draw.rect(pantalla, (50, 220, 80), r_meta)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
