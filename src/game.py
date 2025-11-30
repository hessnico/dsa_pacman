import pygame

from src import constants
from src.logger import log
from src.mapa import Mapa
from src.pacman import Pacman


class Game:
    def __init__(self, m: Mapa, p: Pacman):
        self.mapa = m
        self.pacman = p

        pygame.init()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill("black")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(5) / 1000
            self._polling_eventos()
            self._movimentar(dt)
            self._renderizar_mapa()
            self._acabou()

        pygame.quit()

    def _acabou(self) -> bool:
        if self.pacman.pontuacao >= self.mapa.max_pontos:
            log.Info(f"vitória. pontuação final: {self.pacman.pontuacao}")
            self.running = False
            return True

        return False

    def _polling_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _movimentar(self, dt):
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

        self.pacman.atualizar_invencibilidade(dt)
        if dx != 0 or dy != 0:
            self.pacman.mover(self.mapa, dx, dy)

    def _renderizar_mapa(self):
        self.mapa.renderizar(self.pacman, self.screen)
        self._informa_jogador()
        pygame.display.flip()

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
