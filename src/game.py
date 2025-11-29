import pygame

from src.logger import log
from src.mapa import Mapa
from src.pacman import Pacman


class Game:
    def __init__(self, m: Mapa, p: Pacman):
        self.mapa = m
        self.pacman = p

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill("black")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(5) / 1000
            self._polling_eventos()
            self._movimentar()
            self._renderizar_mapa()
            self.acabou()

        pygame.quit()

    def acabou(self) -> bool:
        if self.pacman.pontuacao >= self.mapa.max_pontos:
            log.Info(f"vitória. pontuação final: {self.pacman.pontuacao}")
            self.running = False
            return True

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
        else:
            return

        self.pacman.mover(self.mapa, dx, dy)

    def _renderizar_mapa(self):
        self.mapa.renderizar(self.pacman, self.screen)
        pygame.display.flip()
