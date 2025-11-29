from __future__ import annotations

import pygame
from typing import TYPE_CHECKING
import src.constants as cst
from src.logger import log

if TYPE_CHECKING:
    from pacman import Pacman


class Mapa:
    def __init__(self, arquivo: str):
        self.grid = []
        self.rows = 0
        self.cols = 0

        self.carregar_arquivo(arquivo)
        self.max_pontos = self.calcular_pontos_maximos()

    def carregar_arquivo(self, caminho: str):
        with open(caminho, "r", encoding="utf-8") as f:
            primeira_linha = f.readline().strip()
            resto = primeira_linha.split()

            self.rows = int(resto[0])
            self.cols = int(resto[1])

            linhas = []
            for _ in range(self.rows):
                linha = f.readline().rstrip("\n")
                linhas.append(linha)

            self.grid = [list(linha) for linha in linhas]

    def calcular_pontos_maximos(self) -> int:
        """
        Calcula a pontuação máxima possível do mapa.
        Cada ponto '.' ou '0' vale 10 pontos.
        Feita para otimizar o encerramento do jogo.
        """
        pontos = 0
        for linha in self.grid:
            for celula in linha:
                if celula in [".", "0"]:
                    pontos += cst.PONTUACAO_PADRAO

        log.Info(f"Mapa inicializado com um total de {pontos} pontos")
        return pontos

    def eh_ponto(self, x, y) -> bool:
        return self.grid[x][y] == "."

    def eh_powerup(self, x, y) -> bool:
        return self.grid[x][y] == "0"

    def remover_ponto(self, x, y) -> bool:
        if self.grid[x][y] in [".", "0"]:
            self.grid[x][y] = " "
            return True

        return False

    def eh_parede(self, x, y) -> bool:
        return self.grid[x][y] == "#"

    def renderizar(self, pacman: Pacman, screen):
        screen.fill("black")

        for row, linha in enumerate(self.grid):
            for col, celula in enumerate(linha):
                x = col * cst.TILE
                y = row * cst.TILE

                match celula:
                    case "#":
                        pygame.draw.rect(screen, cst.BLUE, (x, y, cst.TILE, cst.TILE))

                    case ".":
                        cx = x + cst.TILE // 2
                        cy = y + cst.TILE // 2
                        pygame.draw.circle(screen, cst.YELLOW, (cx, cy), cst.DOT_RADIUS)

        pcx = pacman.y * cst.TILE + cst.TILE // 2
        pcy = pacman.x * cst.TILE + cst.TILE // 2
        pygame.draw.circle(screen, cst.YELLOW, (pcx, pcy), cst.PACMAN_RADIUS)
