from typing import Tuple
from src.pacman import Pacman
from src.mapa import Mapa
from src.logger import log
import argparse

MOVIMENTOS = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1),
}


# colocar debug para facilitar nossa vida
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Ativa logs de debug")
    return parser.parse_args()


def main():
    args = parse_args()
    log.set_debug(args.debug)

    m, p = inicializa()
    jogo(m, p)


def jogo(m: Mapa, p: Pacman) -> None:
    while True:
        m.imprimir(p)

        cmd = input("Movimento (WASD, Q para sair): ").lower()

        if cmd == "q":
            log.Info("Saindo")
            break

        if cmd in MOVIMENTOS:
            dx, dy = MOVIMENTOS[cmd]
            p.mover(m, dx, dy)
        else:
            log.Warn(f"Comando inválido: {cmd}")


def inicializa() -> Tuple[Mapa, Pacman]:
    m = Mapa()
    p = Pacman(11, 9)
    arquivo = "./mapas/fase1.txt"
    m.carregar_arquivo(arquivo)

    return m, p


if __name__ == "__main__":
    main()
