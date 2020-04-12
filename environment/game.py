from abc import ABC, abstractmethod


class Game(ABC):
    """
    Abstract game class
    """

    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Nim(Game):
    """
    Remove pieces from a nondescript board until a player removes the last piece.
    """

    def __init__(self, n, k):
        """
        Initialize a two-player nim game with n pieces where a player can remove max k pieces each turn.
        Must support games where 100 > N > K > 1
        :param n: Number of pieces on the board
        :param k: Maximum pieces a player can take off the board on their turn
        """
        super(Nim, self).__init__()
        #
        self.N = n
        self.K = k


class Ledge(Game):
    """
    A one-dimensional board divided into cells, each of which may be empty or may contain coins of either type
    1 (copper) or type 2 (gold). There is only ONE gold coin, while there can be many copper coins (or none
    at all). No more than one coin per cell.
    """

    def __init__(self, board):
        """
        Initialize the one-dimensional board
        :param board: list[int] - Initial board configurations TODO: Or maybe string
        """
        super(Ledge, self).__init__()
        self.board = board
