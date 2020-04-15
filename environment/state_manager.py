from game import Nim, Ledge
from utils import get_new_game
from tree_node import Node


class StateManager:

    def __init__(self, game_type, game_config):
        self.game_type = game_type
        self.game_config = game_config
        self.game = None

    def init_new_game(self):
        self.game = get_new_game(self.game_type, self.game_config, verbose=False)

    def get_child_nodes(self, state):
        """
        Return a list of child nodes for that state
        :param state:
        :return:
        """
        legal_actions = self.game.get_legal_actions(state)
        new_states = [self.game.get_next_state(state, action) for action in legal_actions]
        return [Node(state, action) for state, action in zip(new_states, legal_actions)]

    def is_winning_state(self, state):
        return self.game.verify_winning_state(state)
