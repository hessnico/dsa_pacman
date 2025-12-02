from dataclasses import dataclass

import pygame


@dataclass
class RecursosRenderizacao:
    screen: pygame.Surface
    font: pygame.font.Font
    fonte_titulo: pygame.font.Font
    fonte_instrucao: pygame.font.Font
    clock: pygame.time.Clock
    imagem_pacman: pygame.Surface
    imagem_fantasma: pygame.Surface
