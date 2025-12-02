from typing import List

import pygame

import src.constants as cst
from src import constants
from src.ghost import Fantasma
from src.logger import log
from src.mapa import Mapa
from src.pacman import Pacman


class Game:
    def __init__(self, m: Mapa, p: Pacman, f: List[Fantasma], screen=None):
        self.state = "MENU"

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
            self.screen = pygame.display.set_mode((1280, 1280))

        self.clock = pygame.time.Clock()
        self.running = True

        self.imagem_pacman = pygame.image.load("./imgs/pacman.gif")
        self.imagem_fantasma = pygame.image.load("./imgs/ghost.gif")

    def run(self):
        while self.running:
            if self.state == "MENU":
                self.menu_principal()
            else:
                dt = self.clock.tick(5) / 1000
                self.polling_eventos()
                self.atualizar(dt)
                self.checar_colisoes()
                self.movimentar()
                self.checar_colisoes()
                self.renderizar_mapa()
                self.acabou()

        pygame.quit()

    def menu_principal(self):
        menu = True

        while menu:
            self.screen.fill("black")
            largura, altura = self.screen.get_size()

            titulo_texto = self.fonte_titulo.render("PAC-MAN", True, constants.YELLOW)
            rect_titulo = titulo_texto.get_rect(center=(largura / 2, altura / 2 - 100))
            self.screen.blit(titulo_texto, rect_titulo)

            instrucao_texto = self.fonte_instrucao.render(
                "Pressione ENTER para Começar", True, constants.WHITE
            )
            rect_instrucao = instrucao_texto.get_rect(
                center=(largura / 2, altura / 2 + 50)
            )
            self.screen.blit(instrucao_texto, rect_instrucao)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.entrar_no_jogo()
                        menu = False

    def entrar_no_jogo(self):
        self.clock.tick()
        self.state = "JOGANDO"

    def atualizar(self, dt):
        self.pacman.atualizar_invencibilidade(dt)
        [f.atualizar_tempos(dt) for f in self.fantasmas]

    def colidiu(self, f: Fantasma):
        if self.pacman.x == f.x and self.pacman.y == f.y:
            return True

    def checar_colisoes(self):
        for f in self.fantasmas:
            if self.colidiu(f):
                self.resolver_colisao(f)

    def resolver_colisao(self, f: Fantasma):
        if self.pacman.tempo_invencibilidade > 0:
            f.resetar_posicao()
            return

        self.pacman.vidas -= 1
        log.Info("Pacman perdeu uma vida!")

        self.pacman.resetar_posicao()
        for f in self.fantasmas:
            f.resetar_posicao()

        pygame.time.delay(1500)

    def acabou(self) -> bool:
        if self.pacman.pontuacao >= self.mapa.max_pontos:
            log.Info(f"vitória. pontuação final: {self.pacman.pontuacao}")
            self.mostrar_game_over(
                "VITÓRIA!", cst.GREEN if hasattr(cst, "GREEN") else (0, 255, 0)
            )
            self.running = False
            return True

        if self.pacman.vidas <= 0:
            log.Info("Game Over!")
            self.mostrar_game_over(
                "GAME OVER", cst.RED if hasattr(cst, "RED") else (255, 0, 0)
            )
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

    def polling_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def movimentar(self):
        dx_input = dy_input = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx_input = -1
        elif keys[pygame.K_s]:
            dx_input = 1
        elif keys[pygame.K_a]:
            dy_input = -1
        elif keys[pygame.K_d]:
            dy_input = 1

        [
            f.mover(
                self.mapa,
                self.pacman.tempo_invencibilidade > 0,
                (int(self.pacman.x), int(self.pacman.y)),
            )
            for f in self.fantasmas
        ]

        if dx_input != 0 or dy_input != 0:
            self.pacman.mudar_direcao(dx_input, dy_input, self.mapa)

        self.pacman.mover(self.mapa)

    def renderizar_mapa(self):
        self.renderizar(self.pacman, self.fantasmas, self.screen)
        self.informa_jogador()
        pygame.display.flip()

    def renderizar(self, p: Pacman, fs: List[Fantasma], screen):
        screen.fill("black")

        for row, linha in enumerate(self.mapa.grid):
            for col, celula in enumerate(linha):
                x = col * cst.TILE
                y = row * cst.TILE

                match celula:
                    case "#":
                        self.renderiza_parede(x, y, screen)
                    case ".":
                        self.renderiza_pontinho(x, y, p, screen)
                    case "0":
                        self.renderiza_powerup(x, y, screen)
                    case "<":
                        self.renderiza_pacman(p, screen)
                    case "F":
                        [self.renderiza_fantasma(f, screen) for f in fs]

    def informa_jogador(self):
        altura_grid = len(self.mapa.grid) * constants.TILE
        margem = 10
        y_info = altura_grid + margem
        pont_text = self.font.render(
            f"Pontuação: {self.pacman.pontuacao}", True, constants.WHITE
        )
        vidas_text = self.font.render(
            f"Vidas: {self.pacman.vidas}", True, constants.WHITE
        )

        self.screen.blit(pont_text, (10, y_info))
        self.screen.blit(vidas_text, (200, y_info))

        if self.pacman.tempo_invencibilidade > 0:
            invencibilidade_text = self.font.render(
                f"Invencibilidade: {round(self.pacman.tempo_invencibilidade, 3)}",
                True,
                constants.WHITE,
            )
            self.screen.blit(invencibilidade_text, (400, y_info))

    def renderiza_fantasma(self, f: Fantasma, screen):
        x = f.y * cst.TILE
        y = f.x * cst.TILE
        if hasattr(self, "imagem_fantasma"):
            self.renderiza_imagem_centralizada(x, y, self.imagem_fantasma, screen)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, cst.TILE, cst.TILE))

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
        if hasattr(self, "imagem_pacman"):
            self.renderiza_imagem_centralizada(x, y, self.imagem_pacman, screen)
        else:
            pygame.draw.circle(screen, (255, 255, 0), (x + 16, y + 16), 16)

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

        texto_t = self.fonte_titulo.render(titulo, True, cor_titulo)
        texto_i = self.fonte_instrucao.render(
            "ENTER para Reiniciar ou ESC para Sair", True, constants.WHITE
        )

        rect_t = texto_t.get_rect(center=(largura / 2, altura / 2 - 50))
        rect_i = texto_i.get_rect(center=(largura / 2, altura / 2 + 50))

        tela.blit(texto_t, rect_t)
        tela.blit(texto_i, rect_i)

        pygame.display.flip()
