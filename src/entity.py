from abc import abstractmethod, ABC


class Entidade(ABC):
    def __init__(self, linha: int, coluna: int) -> None:
        self.x: int = linha
        self.y: int = coluna

        self.spawn_x: int = linha
        self.spawn_y: int = coluna

    @abstractmethod
    def mover(self, mapa, *args, **kwargs):
        pass

    def resetar_posicao(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
