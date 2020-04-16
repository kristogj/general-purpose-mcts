from abc import ABC, abstractmethod
import logging


class Game(ABC):
    """
    Abstract game class
    """

    def __init__(self, verbose):
        self.verbose = verbose

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
        pass

    @abstractmethod
    def get_next_state(self, state, action):
        pass


class Nim(Game):
    """
    Remove pieces from a nondescript board until a player removes the last piece. The player who removes the last
    piece wins.
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
        :return: None
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
        :return: list[int] - List of how many stones that can be removed from the board.
        """
        if state == 0:
            return []
        return list(range(1, min(state, self.K) + 1))

    def get_next_state(self, state, action):
        """
        Perform action on given state, and return new state
        :param state: int - How many stones are on the board
        :param action: int - How many stones should be removed from the board
        :return: int - How many stones are left on the board
        """
        self.N = state
        self.perform_action(None, action)
        return self.N

    def get_current_state(self):
        """
        Current state of a Nim game can be represented by just the number of stones left on the board
        :return: int
        """
        return self.N

    def is_winning_state(self):
        """
        Check if there are no more stones left on the board.
        :return: boolean
        """
        return self.N == 0

    @staticmethod
    def verify_winning_state(state):
        """
        Given a state (in this case it state == #stones left), check if it is a winning state
        :param state: int
        :return: boolean
        """
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
        :param board: list[int] - initial board configurations
        """
        super(Ledge, self).__init__(verbose)
        self.board = board
        self.coins = {2: "gold", 1: "copper"}

        if verbose:
            logging.info("Start Board: {}".format(board))

    def perform_action(self, player, action):
        """
        Perform action on the current board being played.
        :param player: int - Player who made the move
        :param action: str - Defines an action as either "P" or "M-x-y" where x and y are integers.
        :return: None
        """
        log_text = ""
        if action == "P":
            coin = self.board[0]
            self.board[0] = 0
            log_text = "P{} picks up {}: {}".format(player, self.coins[coin], self.board)
        elif action.startswith("M"):
            _from, _to = action.split("-")[1:]
            _from, _to = int(_from), int(_to)
            coin = self.board[_from]
            self.board[_from], self.board[_to] = self.board[_to], self.board[_from]
            log_text = "P{} moves {} from cell {} to {}: {}".format(player, self.coins[coin], _from, _to, self.board)

        if self.verbose:
            logging.info(log_text)
            if self.is_winning_state():
                logging.info("Player {} wins".format(player))

    def get_legal_actions(self, state):
        """
        Given a state, return all legal actions from that state.
        A player can make two kind of moves:
            a) (P)ick up the coin at index 0 (the ledge)
                "P" means pick up the coin at the ledge, leaving it an empty cell.
            b) (M)ove a coin to the left between its current position and its left-nearest-neighbour
                "M-X-Y" where X and Y are two integers, means that you should move coin on index X to index Y.
        :param state: int - How many stones are left on the board
        :return: list[int]
        """
        legal_actions = []
        if state[0] > 0:
            legal_actions.append("P")  # Add the pick-up move if a coin is at the ledge

        for i in reversed(range(len(state))):
            if state[i] > 0:
                j = i - 1
                while state[j] == 0 and j >= 0:
                    legal_actions.append("M-{}-{}".format(i, j))
                    j -= 1
        return legal_actions

    def get_next_state(self, state, action):
        """
        Perform action on given state, and return new state
        :param state:
        :param action:
        :return:
        """
        self.board = state.copy()
        self.perform_action(None, action)
        return self.board.copy()  # Return a copy of the board

    def get_current_state(self):
        """
        Current state of a Ledge game can be represented by the board.
        :return: int
        """
        return self.board.copy()  # Return a copy of the board

    def is_winning_state(self):
        """
        Check if the current board has a gold coin on it. If not, the player who moved it of the board won.
        :return: boolean
        """
        return 2 not in set(self.board)

    @staticmethod
    def verify_winning_state(state):
        """
        Given a state (in this case a 1d board), check if it is a winning state
        :param state: list[int]
        :return: boolean
        """
        return 2 not in set(state)

    def __str__(self):
        return "LEDGE board={}".format(self.board)
