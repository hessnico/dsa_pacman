from dataclasses import dataclass
from typing import List

from src.game import Game
from src.ghost import Fantasma
from src.logger import log
from src.mapa import Mapa
from src.pacman import Pacman


@dataclass
class InfoGame:
    mapa: Mapa
    pacman: Pacman
    ghosts: List[Fantasma]


class Orchestrator:
    def __init__(self) -> None:
        pass

    def inicializa(self) -> Exception | None:
        try:
            self.orquestrar_jogo()
            self.orquestrar_ranking()
            return None
        except Exception as e:
            return e

    def orquestrar_jogo(self):
        log.Info("Inicializando o jogo")
        fase_1 = self.inicializa_fase_1()
        fase_2 = self.inicializa_fase_2()
        fase_3 = self.inicializa_fase_3()

        fases = [fase_1, fase_2, fase_3]
        try:
            for f in fases:
                g = Game(f.mapa, f.pacman, f.ghosts)
                g.run()
                if self.devo_parar_jogo(g):
                    log.Info("Jogo finalizado com sucesso. Usuário perdeu")

        except Exception as e:
            log.Error(f"Erro: {e}")

    def orquestrar_ranking(self):
        pass

    def devo_parar_jogo(self, g: Game) -> bool:
        if g.pacman.vidas <= 0:
            return True
        else:
            return False

    def inicializa_fase_1(self) -> InfoGame:
        arquivo = "./mapas/fase1.txt"
        m = Mapa(arquivo)
        p = Pacman(11, 9)
        l_f = [Fantasma(7, 8), Fantasma(7, 9), Fantasma(7, 10), Fantasma(7, 11)]

        return InfoGame(m, p, l_f)

    def inicializa_fase_2(self) -> InfoGame:
        arquivo = "./mapas/fase2.txt"
        m = Mapa(arquivo)
        p = Pacman(16, 8)
        l_f = [Fantasma(8, 8), Fantasma(8, 9), Fantasma(8, 10), Fantasma(8, 11)]

        return InfoGame(m, p, l_f)

    def inicializa_fase_3(self) -> InfoGame:
        arquivo = "./mapas/fase3.txt"
        m = Mapa(arquivo)
        p = Pacman(25, 14)
        l_f = [Fantasma(13, 11), Fantasma(13, 13), Fantasma(13, 14), Fantasma(13, 16)]

        return InfoGame(m, p, l_f)
