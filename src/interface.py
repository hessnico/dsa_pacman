import pygame
from src import constants

class Interface:
    def __init__(self):
        pygame.font.init()
        
        self.fonte_hud = pygame.font.SysFont("Arial", 24, bold=True)
        self.fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
        self.fonte_instrucao = pygame.font.SysFont("Arial", 25)

    def desenhar_hud(self, tela, pacman, mapa):
        altura_grid = len(mapa.grid) * constants.TILE
        margem = 10
        y_info = altura_grid + margem

        texto_pontos = self.fonte_hud.render(f"SCORE: {pacman.pontuacao}", True, constants.WHITE)
        tela.blit(texto_pontos, (10, y_info))

        texto_vidas = self.fonte_hud.render(f"VIDAS: {pacman.vidas}", True, constants.WHITE)
        tela.blit(texto_vidas, (200, y_info))

        if pacman.tempo_invencibilidade > 0:
            texto_inv = self.fonte_hud.render(
                f"INVENCÍVEL: {round(pacman.tempo_invencibilidade, 1)}s", 
                True, constants.WHITE
            )
            tela.blit(texto_inv, (400, 10))

    def desenhar_tela_fim(self, tela, titulo, cor_titulo):
        largura, altura = tela.get_size()

        overlay = pygame.Surface((largura, altura))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        texto_t = self.fonte_titulo.render(titulo, True, cor_titulo)
        texto_i = self.fonte_instrucao.render("ENTER para Reiniciar ou ESC para Sair", True, constants.WHITE)

        rect_t = texto_t.get_rect(center=(largura/2, altura/2 - 50))
        rect_i = texto_i.get_rect(center=(largura/2, altura/2 + 50))

        tela.blit(texto_t, rect_t)
        tela.blit(texto_i, rect_i)
        
        pygame.display.flip()