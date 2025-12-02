import heapq
import json
from enum import Enum
from dataclasses import dataclass
from typing import List
import os
from src.logger import log
from src import constants


@dataclass(order=True)
class Ranking:
    pontos: int
    usuario: str


class StatusOpRanking(Enum):
    SUCESSO = "sucesso ao salvar arquivo de ranking"
    ERRO = "erro ao salvar arquivo de ranking"
    ARQUIVO_NAO_EXISTENTE = "Arquivo não existe"


class RankingMaxHeap:
    def __init__(self, pontos: int, usuario: str):
        self.new_entry: Ranking = Ranking(pontos=pontos, usuario=usuario)
        self.heap: List[Ranking] = []

    def salva_ranking(self):
        status = self.carregar()
        if status != StatusOpRanking.SUCESSO:
            log.Error(f"Erro: {status.value}")
            return status

        self.transformar()
        return self.salvar()

    def transformar(self) -> None:
        self.heap.append(self.new_entry)

        # Transform list into a maxheap, in-place, in O(len(x)) time.
        # -> O(n)
        heapq._heapify_max(self.heap)
        log.Debug(f"heap depois do heapify_max: {self.heap}")

    def carregar(self) -> StatusOpRanking:
        if not os.path.exists(constants.PATH_RANKING):
            return StatusOpRanking.ARQUIVO_NAO_EXISTENTE

        try:
            with open(constants.PATH_RANKING, "r") as f:
                data = json.load(f)

            log.Info("JSON carregado com sucesso")
            for d in data:
                self.heap.append(Ranking(pontos=d["pontos"], usuario=d["usuario"]))
                log.Debug(f"carregado: {d}")

            return StatusOpRanking.SUCESSO

        except Exception as e:
            log.Error(f"Erro ao carregar ranking: {e}")
            return StatusOpRanking.ERRO

    def salvar(self) -> StatusOpRanking:
        try:
            log.Info("Iniciar salvamento local do ranking")
            data = [{"usuario": r.usuario, "pontos": r.pontos} for r in self.heap]
            log.Debug(f"Salvando: {data}")

            with open(constants.PATH_RANKING, "w") as f:
                json.dump(data, f, indent=4)

            return StatusOpRanking.SUCESSO

        except Exception as e:
            log.Error(f"Erro ao salvar ranking: {e}")
            return StatusOpRanking.ERRO
