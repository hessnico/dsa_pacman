from typing import Tuple


class Mapa:
    def __init__(self):
        self.grid = []
        self.rows = 0
        self.cols = 0

    def carregar_arquivo(self, caminho: str):
        with open(caminho, "r", encoding="utf-8") as f:
            primeira_linha = f.readline().strip()
            partes = primeira_linha.split()

            if len(partes) != 2:
                raise ValueError(
                    "A primeira linha do arquivo deve conter: <rows> <cols>"
                )

            self.rows = int(partes[0])
            self.cols = int(partes[1])

            linhas = []
            for _ in range(self.rows):
                linha = f.readline().rstrip("\n")

                if len(linha) != self.cols:
                    raise ValueError(
                        f"Linha inválida no mapa: esperado {self.cols} colunas, recebido {len(linha)}."
                    )

                linhas.append(linha)

            self.grid = [list(linha) for linha in linhas]

    def imprimir(self, pacman_pos: Tuple[int, int]) -> None:
        for r in range(self.rows):
            linha = ""
            for c in range(self.cols):
                if pacman_pos and pacman_pos == (r, c):
                    linha += "P"
                else:
                    linha += self.grid[r][c]

            print(linha)
