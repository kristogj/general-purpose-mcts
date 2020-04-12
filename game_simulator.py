from game import Nim, Ledge
import logging


class GameSimulator:
    """
    The simulator must provide these results:
        Play-by-Play game action when in verbose mode
    """

    def __init__(self, config):
        logging.info("Initializing GameSimulator")
        self.game_type = config["game_type"]
        self.batch_size = config["batch_size"]
        self.starting_player = config["starting_player"]
        self.num_sim = config["number_of_simulations_per_game_move"]
        self.verbose = config["verbose"]

    def simulate(self):
        pass
