from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pacman import Pacman


class Mapa:
    def __init__(self):
        self.grid = []
        self.rows = 0
        self.cols = 0

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

    def pegar_item(self, x, y):
        item = self.grid[x][y]
        if item in [".", "0"]:
            self.grid[x][y] = " "

        return item

    def imprimir(self, p: Pacman) -> None:
        for r in range(self.rows):
            linha = ""
            for c in range(self.cols):
                if (p.linha, p.coluna) == (r, c):
                    linha += "<"
                elif self.grid[r][c] == "<":
                    linha += " "
                else:
                    linha += self.grid[r][c]

            print(linha)
