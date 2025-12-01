from typing import Tuple, List
from src.game import Game
from src.ghost import Fantasma
from src.pacman import Pacman
from src.mapa import Mapa
from src.logger import log
import argparse
from dataclasses import dataclass


@dataclass
class InfoGame:
    mapa: Mapa
    pacman: Pacman
    ghosts: List[Fantasma]
    game: Game


# colocar debug para facilitar nossa vida
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Ativa logs de debug")
    return parser.parse_args()


def main():
    args = parse_args()
    log.set_debug(args.debug)

    j = inicializa()
    j.game.run()


def inicializa() -> InfoGame:
    arquivo = "./mapas/fase1.txt"
    m = Mapa(arquivo)
    p = Pacman(11, 9)
    l_f = [Fantasma(1, 2), Fantasma(7, 9), Fantasma(7, 10), Fantasma(7, 11)]
    g = Game(m, p, l_f)

    return InfoGame(m, p, l_f, g)


if __name__ == "__main__":
    main()
