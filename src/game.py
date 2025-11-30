import pygame

from typing import List
from src import constants
from src.ghost import Fantasma
from src.logger import log
from src.mapa import Mapa
from src.pacman import Pacman

import src.constants as cst


class Game:
    def __init__(self, m: Mapa, p: Pacman, f: List[Fantasma]):
        self.mapa: Mapa = m
        self.pacman: Pacman = p
        self.fantasmas: List[Fantasma] = f

        pygame.init()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill("black")
        self.clock = pygame.time.Clock()
        self.running = True

        self.imagem_pacman = pygame.image.load("./imgs/pacman.gif")
        self.imagem_fantasma = pygame.image.load("./imgs/ghost.gif")

    def run(self):
        while self.running:
            dt = self.clock.tick(5) / 1000
            self._polling_eventos()
            self._atualizar(dt)
            self._movimentar()
            self._checar_colisoes()
            self._renderizar_mapa()
            self._acabou()

        pygame.quit()

    def _atualizar(self, dt):
        self.pacman.atualizar_invencibilidade(dt)
        [f.atualizar_tempos(dt) for f in self.fantasmas]

    def _checar_colisoes(self):
        for f in self.fantasmas:
            if f.x == self.pacman.x and f.y == self.pacman.y:
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
            # TODO: voltar ao menu principal
            log.Info("Game Over!")
            self.running = False
            return

        pygame.time.delay(1500)

    def _acabou(self) -> bool:
        if self.pacman.pontuacao >= self.mapa.max_pontos:
            log.Info(f"vitória. pontuação final: {self.pacman.pontuacao}")
            self.running = False
            return True

        if self.pacman.vidas <= 0:
            log.Info(f"Derrota. Pontuação final: {self.pacman.pontuacao}")

        return False

    def _polling_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _movimentar(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w]:
            dx = -1
        elif keys[pygame.K_s]:
            dx = 1
        elif keys[pygame.K_a]:
            dy = -1
        elif keys[pygame.K_d]:
            dy = 1

        [f.mover(self.mapa) for f in self.fantasmas]
        if dx != 0 or dy != 0:
            self.pacman.mover(self.mapa, dx, dy)

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

    def _informa_jogador(self):
        altura_grid = len(self.mapa.grid) * constants.TILE
        margem = 10
        y_info = altura_grid + margem
        pont_text = self.font.render(
            f"Pontuação: {self.pacman.pontuacao}", True, constants.WHITE
        )
        vidas_text = self.font.render(
            f"Vidas: {self.pacman.vidas}", True, constants.WHITE
        )
        invencibilidade_text = self.font.render(
            f"Invencibilidade: {round(self.pacman.tempo_invencibilidade, 3)}",
            True,
            constants.WHITE,
        )
        self.screen.blit(pont_text, (10, y_info))
        self.screen.blit(vidas_text, (200, y_info))
        if self.pacman.tempo_invencibilidade > 0:
            self.screen.blit(invencibilidade_text, (400, y_info))

    def renderiza_fantasma(self, f: Fantasma, screen):
        x = f.y * cst.TILE
        y = f.x * cst.TILE
        self.renderiza_imagem_centralizada(x, y, self.imagem_fantasma, screen)

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
        self.renderiza_imagem_centralizada(x, y, self.imagem_pacman, screen)

    def renderiza_imagem_centralizada(self, x, y, img, screen) -> None:
        w = self.imagem_pacman.get_width()
        h = self.imagem_pacman.get_height()
        offset_x = (cst.TILE - w) // 2
        offset_y = (cst.TILE - h) // 2
        screen.blit(img, (x + offset_x, y + offset_y))
