import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from jugador import Jugador, Disparo
from enemigo import Enemigo


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Ejercicio 2 - Esquivar Enemigos")
    reloj = pygame.time.Clock()

    todos_los_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    disparos = pygame.sprite.Group()

    jugador = Jugador(pantalla.get_rect())
    todos_los_sprites.add(jugador)

    fuente = pygame.font.SysFont(None, 24)
    fuente_grande = pygame.font.SysFont(None, 64)

    timer_enemigo = 0.0
    puntaje = 0.0
    game_over = False

    running = True
    while running:
        dt = reloj.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

        if not game_over:
            teclas = pygame.key.get_pressed()
            todos_los_sprites.update(dt, teclas, disparos)
            disparos.update(dt)

            timer_enemigo += dt
            if timer_enemigo >= 1.0:
                timer_enemigo = 0.0
                nuevo = Enemigo(pantalla.get_rect())
                todos_los_sprites.add(nuevo)
                enemigos.add(nuevo)

            if pygame.sprite.spritecollide(jugador, enemigos, False):
                print("¡Game Over!")
                game_over = True

            colisiones = pygame.sprite.groupcollide(disparos, enemigos, True, True)
            if colisiones:
                puntaje += 10 * len(colisiones)

            puntaje += dt

        pantalla.fill((30, 30, 30))
        todos_los_sprites.draw(pantalla)
        disparos.draw(pantalla)

        fps_texto = fuente.render(f"FPS: {int(reloj.get_fps())}", True, (255, 255, 255))
        pantalla.blit(fps_texto, (10, 10))

        puntaje_texto = fuente.render(f"Puntaje: {int(puntaje)}", True, (255, 255, 255))
        pantalla.blit(puntaje_texto, (10, 35))

        if game_over:
            game_over_texto = fuente_grande.render("¡GAME OVER!", True, (255, 0, 0))
            rect_go = game_over_texto.get_rect(center=(400, 300))
            pantalla.blit(game_over_texto, rect_go)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()