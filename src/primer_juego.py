import pygame
import random

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi Primer Juego")

clock = pygame.time.Clock()

jugador = pygame.Rect(375, 275, 50, 50)
objetivo = pygame.Rect(
    random.randint(0, ANCHO - 50),
    random.randint(0, ALTO - 50),
    50,
    50,
)

velocidad = 1300
color_jugador = (0, 0, 255)
color_objetivo = (255, 0, 0)
color_fondo = (17, 153, 41)
color_texto = (255, 255, 255)

puntaje = 0

fuente = pygame.font.Font(None, 30)

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        jugador.x -= velocidad * dt
    if keys[pygame.K_RIGHT]:
        jugador.x += velocidad * dt
    if keys[pygame.K_UP]:
        jugador.y -= velocidad * dt
    if keys[pygame.K_DOWN]:
        jugador.y += velocidad * dt

    jugador.clamp_ip(pantalla.get_rect())

    if jugador.colliderect(objetivo):
        puntaje += 1
        objetivo.x = random.randint(0, ANCHO - objetivo.width)
        objetivo.y = random.randint(0, ALTO - objetivo.height)

    pantalla.fill(color_fondo)
    pygame.draw.rect(pantalla, color_jugador, jugador)
    pygame.draw.rect(pantalla, color_objetivo, objetivo)

    fps_texto = fuente.render(f"FPS: {int(clock.get_fps())}", True, color_texto)
    puntos_texto = fuente.render(f"Puntos: {puntaje}", True, color_texto)
    pantalla.blit(fps_texto, (10, 10))
    pantalla.blit(puntos_texto, (10, 40))

    pygame.display.flip()

pygame.quit()
