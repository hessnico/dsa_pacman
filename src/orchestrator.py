from dataclasses import dataclass
from enum import Enum
from typing import List

from src import constants
from src.game import Game
from src.ghost import Fantasma
from src.logger import log
from src.mapa import Mapa
from src.pacman import Pacman
from src.ranking import RankingMaxHeap, StatusOpRanking


class StatusJogo(Enum):
    SUCESSO = "sucesso"
    ACABOU_VIDAS = "acabou_vidas"
    ERRO = "erro"


@dataclass
class InfoOrc:
    status: StatusJogo
    pontos: int


@dataclass
class InfoGame:
    mapa: Mapa
    pacman: Pacman
    ghosts: List[Fantasma]


class Orchestrator:
    def __init__(self) -> None:
        pass

    def inicializa(self) -> bool:
        jogo_res = self.orquestrar_jogo()
        if jogo_res.status == StatusJogo.ERRO:
            return False

        log.Info(f"Jogo encerrado com status: {jogo_res.status.value}")

        rank_res = self.orquestrar_ranking(jogo_res)
        if rank_res != StatusOpRanking.SUCESSO:
            log.Error(f"Erro ao salvar ranking: {rank_res.value}")
            return False

        return True

    def orquestrar_jogo(self) -> InfoOrc:
        log.Info("Inicializando o jogo")

        fases = [
            self.inicializa_fase_1(),
            self.inicializa_fase_2(),
            self.inicializa_fase_3(),
        ]

        pontos: int = 0
        try:
            for f in fases:
                g = Game(f.mapa, f.pacman, f.ghosts)
                g.run()
                pontos = pontos + g.pacman.pontuacao
                if self.devo_parar_jogo(g):
                    log.Info("Jogo finalizado com sucesso. Usuário perdeu")
                    return InfoOrc(StatusJogo.ACABOU_VIDAS, pontos)

            return InfoOrc(StatusJogo.SUCESSO, pontos)

        except Exception as e:
            log.Error(f"Erro: {e}")

            # se ocorrer um erro, invalida pontuação
            return InfoOrc(StatusJogo.ERRO, 0)

    def orquestrar_ranking(self, infoOrc: InfoOrc) -> StatusOpRanking:
        log.Info("Salvando logs")
        user = "teste"
        r = RankingMaxHeap(infoOrc.pontos, user)

        return r.salva_ranking()

    def devo_parar_jogo(self, g: Game) -> bool:
        if g.pacman.vidas <= 0:
            return True
        else:
            return False

    def inicializa_fase_1(self) -> InfoGame:
        m = Mapa(constants.PATH_FASE_1)
        p = Pacman(11, 9)
        l_f = [Fantasma(7, 8), Fantasma(7, 9), Fantasma(7, 10), Fantasma(7, 11)]

        return InfoGame(m, p, l_f)

    def inicializa_fase_2(self) -> InfoGame:
        m = Mapa(constants.PATH_FASE_2)
        p = Pacman(16, 8)
        l_f = [Fantasma(8, 8), Fantasma(8, 9), Fantasma(8, 10), Fantasma(8, 11)]

        return InfoGame(m, p, l_f)

    def inicializa_fase_3(self) -> InfoGame:
        m = Mapa(constants.PATH_FASE_3)
        p = Pacman(25, 14)
        l_f = [Fantasma(13, 11), Fantasma(13, 13), Fantasma(13, 14), Fantasma(13, 16)]

        return InfoGame(m, p, l_f)
