from dataclasses import dataclass
from enum import Enum
from typing import List

import pygame

from src import constants
from src.render import RecursosRenderizacao
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
        pygame.init()

        self.recursosRenderizar = RecursosRenderizacao(
            screen=pygame.display.set_mode((1280, 1280)),
            font=pygame.font.SysFont("Arial", 24, bold=True),
            fonte_titulo=pygame.font.SysFont("Arial", 60, bold=True),
            fonte_instrucao=pygame.font.SysFont("Arial", 25),
            clock=pygame.time.Clock(),
            imagem_pacman=pygame.image.load("./imgs/pacman.gif"),
            imagem_fantasma=pygame.image.load("./imgs/ghost.gif"),
        )

    def inicializa(self) -> bool:
        self.menu_principal()

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
                g = Game(f.mapa, f.pacman, f.ghosts, self.recursosRenderizar)
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
        r = RankingMaxHeap(infoOrc.pontos, self.nome_usuario, self.recursosRenderizar)

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

    def _pegar_nome_usuario(self):
        nome = ""
        ativo = True

        while ativo:
            self.recursosRenderizar.screen.fill("black")
            largura, altura = self.recursosRenderizar.screen.get_size()

            texto = self.recursosRenderizar.fonte_instrucao.render(
                "Digite seu nome:", True, constants.WHITE
            )
            rect_texto = texto.get_rect(center=(largura / 2, altura / 2 - 40))
            self.recursosRenderizar.screen.blit(texto, rect_texto)

            nome_texto = self.recursosRenderizar.fonte_instrucao.render(
                nome, True, constants.YELLOW
            )
            rect_nome = nome_texto.get_rect(center=(largura / 2, altura / 2 + 10))
            self.recursosRenderizar.screen.blit(nome_texto, rect_nome)

            instr = self.recursosRenderizar.fonte_instrucao.render(
                "ENTER para confirmar", True, constants.WHITE
            )
            rect_instr = instr.get_rect(center=(largura / 2, altura / 2 + 60))
            self.recursosRenderizar.screen.blit(instr, rect_instr)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and nome.strip():
                        self.nome_usuario = nome.strip()
                        ativo = False

                    elif event.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]

                    else:
                        if len(nome) < 15:
                            nome += event.unicode

    def menu_principal(self):
        while True:
            self.recursosRenderizar.screen.fill("black")
            largura, altura = self.recursosRenderizar.screen.get_size()

            titulo_texto = self.recursosRenderizar.fonte_titulo.render(
                "PAC-MAN", True, constants.YELLOW
            )
            rect_titulo = titulo_texto.get_rect(center=(largura / 2, altura / 2 - 100))
            self.recursosRenderizar.screen.blit(titulo_texto, rect_titulo)

            instrucao_texto = self.recursosRenderizar.fonte_instrucao.render(
                "Pressione ENTER para Começar", True, constants.WHITE
            )
            rect_instrucao = instrucao_texto.get_rect(
                center=(largura / 2, altura / 2 + 50)
            )
            self.recursosRenderizar.screen.blit(instrucao_texto, rect_instrucao)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self._pegar_nome_usuario()
                        self.recursosRenderizar.clock.tick()
                        return
