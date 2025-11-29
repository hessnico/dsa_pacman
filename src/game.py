from typing import Tuple

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
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(5) / 1000
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
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
        if dx != 0 or dy != 0:
            self.pacman.mover(self.mapa, dx, dy)

    def render(self):
        self.mapa.renderizar(self.pacman, self.screen)
        pygame.display.flip()
