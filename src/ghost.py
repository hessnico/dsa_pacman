from src.entity import Entidade
import random

from src.logger import log
from src.mapa import Mapa
from src.pacman import Pacman


class Fantasma(Entidade):
    def __init__(self, linha: int, coluna: int) -> None:
        super().__init__(linha, coluna)
        self.tempo_para_sair_base: float = 1
        self.vivo = True

    def mover(self, m: Mapa):
        if self.tempo_para_sair_base > 0:
            return

        direcoes = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        direcoes_validas = []
        for d in direcoes:
            novo_x = self.x + d[0]
            novo_y = self.y + d[1]
            if not m.eh_parede(novo_x, novo_y):
                direcoes_validas.append(d)

        dx, dy = random.choice(direcoes_validas)

        novo_x = self.x + dx
        novo_y = self.y + dy

        if m.eh_parede(novo_x, novo_y):
            log.Warn("Jogada invalida.")
            return  # no-op

        log.Debug(f"DEBUG: Movendo Fantasma de {self.y, self.x} para {novo_y, novo_x}")
        self.y = novo_y
        self.x = novo_x

    def resetar_posicao(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.tempo_para_sair_base = 3

    def atualizar_tempos(self, dt):
        if self.tempo_para_sair_base <= 0:
            return

        self.tempo_para_sair_base -= dt
        if self.tempo_para_sair_base <= 0:
            self.tempo_para_sair_base = 0
            log.Info("Invencibilidade terminou")
