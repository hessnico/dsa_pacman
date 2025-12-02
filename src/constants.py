MOVIMENTOS = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1),
}

MOVIMENTOS_LISTA = [(1, 0), (-1, 0), (0, 1), (0, -1)]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARKER_BLUE = (0, 0, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
PUMPKIN_ORANGE = (255, 117, 24)

TILE = 32
SPEED = 200
DOT_RADIUS = TILE // 8
POWERUP_RADIUS = TILE // 4
PACMAN_RADIUS = TILE // 2 - 2

PONTUACAO_PADRAO: int = 10

PATH_RANKING = "./results/resultados.txt"
PATH_FASE_1 = "./mapas/fase1.txt"
PATH_FASE_2 = "./mapas/fase2.txt"
PATH_FASE_3 = "./mapas/fase3.txt"
