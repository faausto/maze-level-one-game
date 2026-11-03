import pygame

pygame.init()
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Cámara de seguimiento")
clock = pygame.time.Clock()

# El jugador vive en COORDENADAS DEL MUNDO (no de la pantalla)
jugador = pygame.Rect(1000, 800, 40, 40)
velocidad = 5

# Objetos fijos del mundo, para notar el desplazamiento
obstaculos = [
    pygame.Rect(800, 700, 100, 100),
    pygame.Rect(1200, 900, 150, 60),
    pygame.Rect(1100, 600, 80, 200),
    pygame.Rect(700, 900, 140, 80),
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        jugador.x -= velocidad
    if keys[pygame.K_RIGHT]:
        jugador.x += velocidad
    if keys[pygame.K_UP]:
        jugador.y -= velocidad
    if keys[pygame.K_DOWN]:
        jugador.y += velocidad

    # LA CÁMARA: offset para centrar al jugador
    offset_y = jugador.centery - ALTO // 2
    offset_x = jugador.centerx - ANCHO // 2

    pantalla.fill((30, 30, 40))

    # Dibujar cada objeto restando el offset
    for obs in obstaculos:
        r = pygame.Rect(obs.x - offset_x, obs.y - offset_y, obs.w, obs.h)
        pygame.draw.rect(pantalla, (100, 200, 120), r)

    # El jugador siempre se ve centrado
    r_jug = pygame.Rect(jugador.x - offset_x, jugador.y - offset_y, jugador.w, jugador.h)
    pygame.draw.rect(pantalla, (240, 200, 80), r_jug)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()