from abc import ABC, abstractmethod
import logging


class Game(ABC):
    """
    Abstract game class
    """

    def __init__(self, verbose):
        self.verbose = verbose
        pass

    @abstractmethod
    def perform_action(self, player, action):
        pass

    @abstractmethod
    def is_winning_state(self):
        pass

    @staticmethod
    @abstractmethod
    def verify_winning_state(state):
        pass

    @abstractmethod
    def get_legal_actions(self, state):
        """
        Given a state, return all legal actions from that state.
        :param state:
        :return:
        """
        pass

    @abstractmethod
    def get_next_state(self, state, action):
        """
        Given a state and an action. Perform the action from that state, and return the new state.
        :param state:
        :param action:
        :return:
        """


class Nim(Game):
    """
    Remove pieces from a nondescript board until a player removes the last piece.
    """

    def __init__(self, n, k, verbose):
        """
        Initialize a two-player nim game with n pieces where a player can remove max k pieces each turn.
        Must support games where 100 > N > K > 1
        :param n: Number of pieces on the board
        :param k: Maximum pieces a player can take off the board on their turn
        """
        super(Nim, self).__init__(verbose)
        self.N = n
        self.K = k

        if verbose:
            logging.info("Start Pile: {} stones".format(n))

    def perform_action(self, player, action):
        """
        Perform the action in the game
        :param player: int - Which player is making the move
        :param action: int - How many stones are removed
        :return:
        """
        self.N -= action
        if self.verbose:
            logging.info("Player {} selects {} stones: Remaining stones = {}".format(player, action, self.N))
            if self.is_winning_state():
                logging.info("Player {} wins".format(player))

    def get_legal_actions(self, state):
        """
        Given a state, return all legal actions from that state.
        :param state: int - How many stones are left on the board
        :return: list[int]
        """
        if state == 0:
            return []
        return list(range(1, min(state, self.K) + 1))

    def get_next_state(self, state, action):
        """
        Perform action on given state, and return new state
        :param state:
        :param action:
        :return:
        """
        self.N = state
        self.perform_action(None, action)
        return self.N

    def get_current_state(self):
        return self.N

    def is_winning_state(self):
        return self.N == 0

    @staticmethod
    def verify_winning_state(state):
        return state == 0

    def __str__(self):
        return "NIM N={} K={}".format(self.N, self.K)


class Ledge(Game):
    """
    A one-dimensional board divided into cells, each of which may be empty or may contain coins of either type
    1 (copper) or type 2 (gold). There is only ONE gold coin, while there can be many copper coins (or none
    at all). No more than one coin per cell.
    """

    def __init__(self, board, verbose):
        """
        Initialize the one-dimensional board
        :param board: string - initial board configurations
        """
        super(Ledge, self).__init__(verbose)
        self.board = board

        if verbose:
            logging.info("Start Board: {}".format(board))

    def perform_action(self, player, action):
        # TODO: Perform action
        if self.verbose:
            logging.info("P1 moves copper from cell 8 to 6: [0 0 0 1 0 2 1 0 0 0]")  # Example
            if self.is_winning_state():
                logging.info("Player {} wins".format(player))

    def is_winning_state(self):
        pass
