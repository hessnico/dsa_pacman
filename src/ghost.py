import random
from collections import deque
from typing import List, Tuple

from src import constants
from src.entity import Entidade
from src.logger import log
from src.mapa import Mapa


class Fantasma(Entidade):
    def __init__(self, linha: int, coluna: int) -> None:
        super().__init__(linha, coluna)
        self.tempo_para_sair_base: float = 2
        self.vivo = True

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

    def mover_bfs(self, m: Mapa, destino: Tuple[int, int]) -> None:
        inicio = (int(self.x), int(self.y))
        alvo = (int(destino[0]), int(destino[1]))

        if inicio == alvo:
            return

        caminho_ate_pacman: List | None = self.bfs(m, inicio, alvo)
        if caminho_ate_pacman is not None and len(caminho_ate_pacman) > 0:
            self.x = caminho_ate_pacman[-1][0]
            self.y = caminho_ate_pacman[-1][1]
        else:
            log.Error("Não encontrou caminho. Algo está errado.")

    def mover(self, m: Mapa, eh_invencivel: bool, destino: Tuple[int, int]):
        if self.tempo_para_sair_base > 0:
            return

        log.Debug(f"eh eh_invencivel: {eh_invencivel}")

        if eh_invencivel:
            self.mover_aleatorio(m)
        else:
            self.mover_bfs(m, destino)

    def bfs(self, m: Mapa, inicio: Tuple, destino: Tuple[int, int]) -> List | None:
        fila = deque()
        fila.append(inicio)

        visitados = set()
        visitados.add(inicio)

        veio_de = {}  # chave do dict serve como aresta e o valor como vertice
        encontrou = False

        while fila:
            atual = fila.popleft()

            if atual == destino:
                encontrou = True
                break

            x, y = atual
            for dx, dy in constants.MOVIMENTOS_LISTA:
                novo_x, novo_y = x + dx, y + dy
                vizinho = (novo_x, novo_y)

                if self.caminho_valido(m, novo_x, novo_y, vizinho, visitados):
                    fila.append(vizinho)
                    visitados.add(vizinho)
                    veio_de[vizinho] = atual

        if encontrou:
            caminho = []
            passo_atual = destino

            while passo_atual != inicio:
                caminho.append(passo_atual)
                passo_atual = veio_de[passo_atual]

            return caminho

        return None

    def caminho_valido(self, m: Mapa, novo_x, novo_y, vizinho, visitados):
        return (
            0 <= novo_x < m.rows
            and 0 <= novo_y < m.cols
            and not m.eh_parede(novo_x, novo_y)
            and vizinho not in visitados
        )

    def mover_aleatorio(self, m: Mapa) -> None:
        direcoes = constants.MOVIMENTOS_LISTA
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
            log.Debug("Jogada invalida.")
            return  # no-op

        log.Debug(f"DEBUG: Movendo Fantasma de {self.y, self.x} para {novo_y, novo_x}")
        self.y = novo_y
        self.x = novo_x
