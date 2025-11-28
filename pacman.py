from mapa import Mapa
from logger import log


class Pacman:
    def __init__(self, linha: int, coluna: int) -> None:
        self.linha = linha
        self.coluna = coluna

    def mover(self, mapa: Mapa, dx: int, dy: int):
        novo_x = self.linha + dx
        novo_y = self.coluna + dy

        if mapa.grid[novo_x][novo_y] == "#":
            log.Warn("Jogada invalida.")
            return  # no-op

        _ = Mapa.pegar_item(mapa, self.linha, self.coluna)

        log.Debug(
            f"DEBUG: Movendo Pacman de {self.coluna, self.linha} para {novo_y, novo_x}"
        )
        self.coluna = novo_y
        self.linha = novo_x
