from typing import Tuple
from src.game import Game
from src.pacman import Pacman
from src.mapa import Mapa
from src.logger import log
import argparse
from dataclasses import dataclass


@dataclass
class InfoGame:
    mapa: Mapa
    pacman: Pacman
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
    m = Mapa()
    p = Pacman(11, 9)
    g = Game(m, p)
    arquivo = "./mapas/fase1.txt"
    m.carregar_arquivo(arquivo)

    return InfoGame(m, p, g)


if __name__ == "__main__":
    main()
