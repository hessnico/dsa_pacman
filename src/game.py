import pygame
import math
from typing import List
from src import constants
from src import pacman
from src.ghost import Fantasma
from src.logger import log
from src.mapa import Mapa
from src.pacman import Pacman
import src.constants as cst

class Game:
    def __init__(self, m: Mapa, p: Pacman, f: List[Fantasma], screen=None):
        self.mapa: Mapa = m
        self.pacman: Pacman = p
        self.fantasmas: List[Fantasma] = f

        pygame.init()
        
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        
        self.fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
        self.fonte_instrucao = pygame.font.SysFont("Arial", 25)

        if screen:
            self.screen = screen
        else:
            self.screen = pygame.display.set_mode((800, 800))
        
        self.clock = pygame.time.Clock()
        self.running = True

        try:
            self.imagem_pacman = pygame.image.load("./imgs/pacman.gif")
            self.imagem_fantasma = pygame.image.load("./imgs/ghost.gif")
        except:
            log.Info("Imagens não encontradas, usando quadrados coloridos.")

    def run(self):
        while self.running:
            dt = self.clock.tick(5) / 1000 
            self._polling_eventos()
            self._atualizar(dt)
            self._checar_colisoes()
            self._movimentar(self.mapa)
            self._checar_colisoes()
            self._renderizar_mapa()
            self._acabou()

        pygame.quit() 

    def _atualizar(self, dt):
        self.pacman.atualizar_invencibilidade(dt)
        [f.atualizar_tempos(dt) for f in self.fantasmas]

    def colidiu(self, f: Fantasma):
        if self.pacman.x == f.x and self.pacman.y == f.y:
            return True

    def _checar_colisoes(self):
        for f in self.fantasmas:
            if self.colidiu(f):
                self._resolver_colisao(f)

    def _resolver_colisao(self, f: Fantasma):
        if self.pacman.tempo_invencibilidade > 0:
            self.pacman.pontuacao += 100
            f.resetar_posicao()
            return

        self.pacman.vidas -= 1
        log.Info("Pacman perdeu uma vida!")

        self.pacman.resetar_posicao()
        for f in self.fantasmas:
            f.resetar_posicao()

        if self.pacman.vidas <= 0:
            log.Info("Game Over!")
            self.mostrar_game_over("GAME OVER", cst.RED if hasattr(cst, 'RED') else (255,0,0))
            self.running = False
            return

        pygame.time.delay(1500)

    def _acabou(self) -> bool:
        if self.pacman.pontuacao >= self.mapa.max_pontos:
            log.Info(f"vitória. pontuação final: {self.pacman.pontuacao}")
            self.mostrar_game_over("VITÓRIA!", cst.GREEN if hasattr(cst, 'GREEN') else (0,255,0))
            self.running = False
            return True

        return False

    def mostrar_game_over(self, mensagem, cor):
        esperando = True
        while esperando:
            self.desenhar_tela_fim(self.screen, mensagem, cor)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esperando = False
                        self.running = False
                    if event.key == pygame.K_RETURN:
                        esperando = False

    def _polling_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _movimentar(self, mapa: Mapa): ##
        dx_input = dy_input = 0 

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: dx_input = -1
        elif keys[pygame.K_s]: dx_input = 1
        elif keys[pygame.K_a]: dy_input = -1
        elif keys[pygame.K_d]: dy_input = 1

        [f.mover(self.mapa) for f in self.fantasmas]
        if dx_input != 0 or dy_input != 0:
            self.pacman.mudar_direcao(dx_input, dy_input, self.mapa)

        self.pacman.mover(self.mapa)

    def _renderizar_mapa(self):
        self._renderizar(self.pacman, self.fantasmas, self.screen)
        self._informa_jogador()
        pygame.display.flip()

    def _renderizar(self, p: Pacman, fs: List[Fantasma], screen):
        screen.fill("black")

        for row, linha in enumerate(self.mapa.grid):
            for col, celula in enumerate(linha):
                x = col * cst.TILE
                y = row * cst.TILE

                match celula:
                    case "#": self.renderiza_parede(x, y, screen)
                    case ".": self.renderiza_pontinho(x, y, p, screen)
                    case "0": self.renderiza_powerup(x, y, screen)
                    case "<": self.renderiza_pacman(p, screen)
                    case "F": [self.renderiza_fantasma(f, screen) for f in fs]

    def _informa_jogador(self):
        altura_grid = len(self.mapa.grid) * constants.TILE
        margem = 10
        y_info = altura_grid + margem
        pont_text = self.font.render(f"Pontuação: {self.pacman.pontuacao}", True, constants.WHITE)
        vidas_text = self.font.render(f"Vidas: {self.pacman.vidas}", True, constants.WHITE)
        
        self.screen.blit(pont_text, (10, y_info))
        self.screen.blit(vidas_text, (200, y_info))
        
        if self.pacman.tempo_invencibilidade > 0:
            invencibilidade_text = self.font.render(
                f"Invencibilidade: {round(self.pacman.tempo_invencibilidade, 3)}",
                True, constants.WHITE,
            )
            self.screen.blit(invencibilidade_text, (400, y_info))

    def renderiza_fantasma(self, f: Fantasma, screen):
        x = f.y * cst.TILE
        y = f.x * cst.TILE
        if hasattr(self, 'imagem_fantasma'):
            self.renderiza_imagem_centralizada(x, y, self.imagem_fantasma, screen)
        else:
            pygame.draw.rect(screen, (255,0,0), (x, y, cst.TILE, cst.TILE))

    def renderiza_pontinho(self, x, y, p, screen):
        cx = x + cst.TILE // 2
        cy = y + cst.TILE // 2
        cor = cst.PURPLE if p.tempo_invencibilidade > 0 else cst.YELLOW
        pygame.draw.circle(screen, cor, (cx, cy), cst.DOT_RADIUS)

    def renderiza_parede(self, x, y, screen):
        pygame.draw.rect(screen, cst.DARKER_BLUE, (x, y, cst.TILE, cst.TILE))

    def renderiza_powerup(self, x, y, screen):
        cx = x + cst.TILE // 2
        cy = y + cst.TILE // 2
        pygame.draw.circle(screen, cst.PUMPKIN_ORANGE, (cx, cy), cst.POWERUP_RADIUS)

    def renderiza_pacman(self, p: Pacman, screen) -> None:
        x = p.y * cst.TILE
        y = p.x * cst.TILE
        if hasattr(self, 'imagem_pacman'):
            self.renderiza_imagem_centralizada(x, y, self.imagem_pacman, screen)
        else:
            pygame.draw.circle(screen, (255,255,0), (x + 16, y + 16), 16)

    def renderiza_imagem_centralizada(self, x, y, img, screen) -> None:
        w = img.get_width()
        h = img.get_height()
        offset_x = (cst.TILE - w) // 2
        offset_y = (cst.TILE - h) // 2
        screen.blit(img, (x + offset_x, y + offset_y))

    def desenhar_tela_fim(self, tela, titulo, cor_titulo):
        largura, altura = tela.get_size()

        overlay = pygame.Surface((largura, altura))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        # Agora usa self.fonte_titulo que criamos no init
        texto_t = self.fonte_titulo.render(titulo, True, cor_titulo)
        texto_i = self.fonte_instrucao.render("ENTER para Reiniciar ou ESC para Sair", True, constants.WHITE)

        rect_t = texto_t.get_rect(center=(largura/2, altura/2 - 50))
        rect_i = texto_i.get_rect(center=(largura/2, altura/2 + 50))

        tela.blit(texto_t, rect_t)
        tela.blit(texto_i, rect_i)
        
        pygame.display.flip()