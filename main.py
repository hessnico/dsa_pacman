from mapa import Mapa
from pacman import Pacman


def main():
    mapa = Mapa()
    mapa.carregar_arquivo("fase1.txt")

    p = Pacman(9, 5)

    mapa.imprimir(pacman_pos=(p.coluna, p.linha))


if __name__ == "__main__":
    main()
