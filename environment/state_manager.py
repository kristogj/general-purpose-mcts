from game import Nim, Ledge


class StateManager:

    def __init__(self, game_type, game_config):
        self.game_type = game_type
        self.game_config = game_config
        self.verbose = game_config["verbose"]
        self.game = None

    def init_new_game(self):
        self.game = self.get_new_game()

    def get_new_game(self):
        if self.game_type == "nim":
            game = Nim(n=self.game_config["Nim"]["n"], k=self.game_config["Nim"]["k"], verbose=self.verbose)
        elif self.game_type == "ledge":
            game = Ledge(self.game_config["Ledge"]["board_init"], verbose=self.verbose)
        else:
            raise ValueError("Game type is not supported")
        return game

    def get_game_state(self):
        pass

    def get_start_states(self):
        pass

    def get_child_states(self, state):
        pass

    def is_winning_state(self, state):
        pass
