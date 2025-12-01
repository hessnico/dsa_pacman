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

        #log.Debug(f"DEBUG: Movendo Fantasma de {self.y, self.x} para {novo_y, novo_x}")
        
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

    def mover(self, m: Mapa, destino: tuple[int, int]):
        if self.tempo_para_sair_base > 0:
            return

        inicio = (int(self.x), int(self.y)) 
        alvo = (int(destino[0]), int(destino[1]))

        if inicio == alvo: return

        if m.eh_parede(alvo[0], alvo[1]):
            log.Info(f"ERRO: O Pacman está dentro da parede em {alvo} ou coordenadas invertidas!")
            return

        caminho_ate_pacman = self.bfs(m, inicio, alvo)
        
        if caminho_ate_pacman is not None and len(caminho_ate_pacman) > 0:
            proximo_passo = caminho_ate_pacman[-1]

            self.x = proximo_passo[0]
            self.y = proximo_passo[1]

        else:
            #self.mover_aleatorio(m)
            log.Warn("Não encontrou caminho")


    def bfs(self, m: Mapa, inicio: tuple, destino: tuple[int, int]):
        from collections import deque

        fila = deque()
        fila.append(inicio)

        visitados = set()
        visitados.add(inicio)

        veio_de = {} # chave do dict serve como aresta e o valor como vertice
        encontrou = False

        while fila: 
            atual = fila.popleft()

            if atual == destino:
                encontrou = True
                break

            x, y = atual
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                novo_x, novo_y = x + dx, y + dy
                vizinho = (novo_x, novo_y)

                if (0 <= novo_x < m.rows and 0 <= novo_y < m.cols and not m.eh_parede(novo_x, novo_y) 
                and vizinho not in visitados):
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

    def mover_aleatorio(self, m: Mapa):
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
        