from src.mapa import Mapa
from src.logger import log


class Pacman:
    def __init__(self, linha: int, coluna: int) -> None:
        self.x = linha
        self.y = coluna

    def mover(self, mapa: Mapa, dx: int, dy: int):
        novo_x = self.x + dx
        novo_y = self.y + dy

        if mapa.eh_parede(novo_x, novo_y):
            log.Warn("Jogada invalida.")
            return  # no-op

        _ = self.pegar_item(mapa)

        log.Debug(f"DEBUG: Movendo Pacman de {self.y, self.x} para {novo_y, novo_x}")
        self.y = novo_y
        self.x = novo_x

    def pegar_item(self, mapa: Mapa):
        if mapa.eh_ponto(self.x, self.y):
            if mapa.remover_ponto(self.x, self.y):
                log.Info("ganhei pontos")
