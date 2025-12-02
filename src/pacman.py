from src.entity import Entidade
from src.logger import log
from src.mapa import Mapa


class Pacman(Entidade):
    def __init__(self, linha: int, coluna: int) -> None:
        super().__init__(linha, coluna)
        self.pontuacao: int = 0
        self.tempo_invencibilidade: float = 0
        self.vidas: int = 1

        self.dx_atual = 0
        self.dy_atual = 0

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

    def mudar_direcao(self, dx: int, dy: int, mapa: Mapa):  ## movimento continuo
        dx_futuro = self.x + dx
        dy_futuro = self.y + dy

        if mapa.eh_parede(dx_futuro, dy_futuro):  ## se for parede, continua com
            self.dx_atual = self.dx_atual
            self.dy_atual = self.dy_atual
        elif dx != 0 or dy != 0:
            self.dx_atual = dx
            self.dy_atual = dy

    def mover(self, mapa: Mapa):
        novo_x = self.x + self.dx_atual
        novo_y = self.y + self.dy_atual

        if mapa.eh_parede(novo_x, novo_y):
            log.Debug("Parede")
            return
        log.Debug(f"DEBUG: Movendo Pacman de {self.y, self.x} para {novo_y, novo_x}")

        _ = self.pegar_item(mapa)

        self.y = novo_y
        self.x = novo_x

    def pegar_item(self, mapa: Mapa):
        if mapa.eh_ponto(self.x, self.y):
            if mapa.remover_ponto(self.x, self.y):
                self.pontua(10)
                log.Debug(f"Pontuação: {self.pontuacao}")
        elif mapa.eh_powerup(self.x, self.y):
            if mapa.remover_ponto(self.x, self.y):
                self.fica_invencivel()
