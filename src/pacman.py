from src.mapa import Mapa
from src.logger import log


class Pacman:
    def __init__(self, linha: int, coluna: int) -> None:
        self.x: int = linha
        self.y: int = coluna
        self.vidas: int = 3
        self.pontuacao: int = 0

    def remove_vida(self) -> None:
        self.vidas -= 1

    def pontua(self, pontos: int) -> None:
        self.pontuacao += pontos

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
        if mapa.eh_ponto(self.x, self.y) or mapa.eh_powerup(self.x, self.y):
            if mapa.remover_ponto(self.x, self.y):
                self.pontua(10)
                log.Info(f"Pontuação: {self.pontuacao}")
