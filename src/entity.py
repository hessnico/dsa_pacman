from abc import abstractmethod, ABC


class Entidade(ABC):
    def __init__(self, linha: int, coluna: int) -> None:
        self.x: int = linha
        self.y: int = coluna

    @abstractmethod
    def mover(self, mapa, *args, **kwargs):
        pass
