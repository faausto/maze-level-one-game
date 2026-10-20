import pygame

def crear_fuente(tamano=36):
    return pygame.font.Font(None, tamano)

def dibujar_hud(pantalla, fuente, puntaje, vidas, tiempo):
    # Puntaje arriba a la izquierda
    txt_puntaje = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(txt_puntaje, (10, 10))
    
    # Vidas arriba a la derecha
    txt_vidas = fuente.render(f"Vidas: {vidas}", True, (255, 120, 120))
    pantalla.blit(txt_vidas, (pantalla.get_width() - 130, 10))
    
    # Tiempo en el centro
    txt_tiempo = fuente.render(f"Tiempo: {int(tiempo)}", True, (255, 255, 120))
    pantalla.blit(txt_tiempo, (pantalla.get_width() // 2 - 60, 10))