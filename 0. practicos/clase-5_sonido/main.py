import pygame
import random

from laberinto import Laberinto
from camara import Camara
import audio
import hud

pygame.init()
audio.inicializar_audio()

TILE = 40
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto con cámara, sonido y HUD")
clock = pygame.time.Clock()

laberinto = Laberinto(TILE)
camara = Camara(ANCHO, ALTO, laberinto.ancho_mundo, laberinto.alto_mundo)

jugador = pygame.Rect(TILE + 5, TILE + 5, 30, 30)
velocidad = 200

meta = pygame.Rect(
    laberinto.ancho_mundo - TILE - 40,
    laberinto.alto_mundo - TILE - 40,
    TILE,
    TILE
)

audio.cargar_musica("assets/sounds/soundtrack.wav")
audio.reproducir_musica(volumen=0.2, loops=-1)

sonido_victoria = audio.cargar_sonido("assets/sounds/victory.mp3")

fuente = hud.crear_fuente(36)

monedas = []
for _ in range(5):
    while True:
        mx = random.randint(1, len(laberinto.mapa[0]) - 2) * TILE
        my = random.randint(1, len(laberinto.mapa) - 2) * TILE
        rect_moneda = pygame.Rect(mx + 5, my + 5, TILE - 10, TILE - 10)
        colision = False
        for p in laberinto.paredes:
            if rect_moneda.colliderect(p):
                colision = True
                break
        if not colision and not rect_moneda.colliderect(jugador) and not rect_moneda.colliderect(meta):
            monedas.append(rect_moneda)
            break

timer_moneda = 0
puntaje = 0
vidas = 3
tiempo = 0

running = True
victoria = False

while running:
    dt = clock.tick(60) / 1000.0
    tiempo += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not victoria:
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -velocidad * dt
        if keys[pygame.K_RIGHT]:
            dx = velocidad * dt
        if keys[pygame.K_UP]:
            dy = -velocidad * dt
        if keys[pygame.K_DOWN]:
            dy = velocidad * dt

        jugador.x += dx
        for p in laberinto.paredes:
            if jugador.colliderect(p):
                if dx > 0:
                    jugador.right = p.left
                elif dx < 0:
                    jugador.left = p.right

        jugador.y += dy
        for p in laberinto.paredes:
            if jugador.colliderect(p):
                if dy > 0:
                    jugador.bottom = p.top
                elif dy < 0:
                    jugador.top = p.bottom

        for moneda in monedas[:]:
            if jugador.colliderect(moneda):
                monedas.remove(moneda)
                puntaje += 10

        timer_moneda += dt
        if timer_moneda >= 5.0:
            timer_moneda = 0
            if len(monedas) < 10:
                for _ in range(3):
                    intentos = 0
                    while intentos < 20:
                        mx = random.randint(1, len(laberinto.mapa[0]) - 2) * TILE
                        my = random.randint(1, len(laberinto.mapa) - 2) * TILE
                        rect_moneda = pygame.Rect(mx + 5, my + 5, TILE - 10, TILE - 10)
                        colision = False
                        for p in laberinto.paredes:
                            if rect_moneda.colliderect(p):
                                colision = True
                                break
                        if not colision and not rect_moneda.colliderect(jugador) and not rect_moneda.colliderect(meta):
                            overlap = False
                            for m in monedas:
                                if rect_moneda.colliderect(m):
                                    overlap = True
                                    break
                            if not overlap:
                                monedas.append(rect_moneda)
                                break
                        intentos += 1

        if jugador.colliderect(meta):
            victoria = True
            if sonido_victoria:
                sonido_victoria.play()
            audio.detener_musica()

    camara.actualizar(jugador)

    pantalla.fill((20, 20, 30))
    laberinto.dibujar(pantalla, camara)

    for moneda in monedas:
        r_moneda = camara.aplicar_rect(moneda)
        pygame.draw.rect(pantalla, (255, 215, 0), r_moneda)

    r_jug = camara.aplicar_rect(jugador)
    pygame.draw.rect(pantalla, (240, 200, 80), r_jug)

    r_meta = camara.aplicar_rect(meta)
    pygame.draw.rect(pantalla, (50, 220, 80), r_meta)

    hud.dibujar_hud(pantalla, fuente, puntaje, vidas, tiempo)

    pygame.display.flip()

    if victoria:
        pygame.time.wait(int(sonido_victoria.get_length() * 1000) if sonido_victoria else 2000)
        running = False

pygame.quit()