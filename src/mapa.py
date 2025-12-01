from __future__ import annotations

import pygame
import src.constants as cst
from src.logger import log


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
                if celula in ["."]:
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
