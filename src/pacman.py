from src.entity import Entidade
from src.mapa import Mapa
from src.logger import log


class Pacman(Entidade):
    def __init__(self, linha: int, coluna: int) -> None:
        super().__init__(linha, coluna)
        self.pontuacao: int = 0
        self.tempo_invencibilidade: float = 0
        self.vidas: int = 3

    def pontua(self, pontos: int) -> None:
        self.pontuacao += pontos

    def fica_invencivel(self) -> None:
        self.tempo_invencibilidade = 10

    def atualizar_invencibilidade(self, dt):
        if self.tempo_invencibilidade <= 0:
            return

        log.Debug(f"Antes de diminuir Invencibilidade: {self.tempo_invencibilidade}")
        self.tempo_invencibilidade -= dt
        log.Debug(f"Depois de diminuir Invencibilidade: {self.tempo_invencibilidade}")
        if self.tempo_invencibilidade <= 0:
            self.tempo_invencibilidade = 0
            log.Info("Invencibilidade terminou")

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
                self.pontua(10)
                log.Info(f"Pontuação: {self.pontuacao}")
        elif mapa.eh_powerup(self.x, self.y):
            if mapa.remover_ponto(self.x, self.y):
                self.fica_invencivel()
