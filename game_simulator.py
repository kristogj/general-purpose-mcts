from game import Nim, Ledge
import logging
from game import Nim, Ledge
from mcts import MonteCarloSearchTree
import random


class GameSimulator:
    """
    The simulator must provide these results:
        Play-by-Play game action when in verbose mode
        Essential win statistics (for at least one of the two players) for a batch of games.
    """

    def __init__(self, config):
        logging.info("Initializing GameSimulator")
        self.game_type = config["game_type"]
        self.batch_size = config["batch_size"]  #
        self.starting_player = config["starting_player"]  # 1 (Player 1), 2 (Player 2), 3 (Random Player)
        self.num_sim = config["num_sim"]
        self.verbose = config["verbose"]

        # Game configs
        self.config_nim = config["Nim"]
        self.config_ledge = config["Ledge"]

    def get_new_game(self):
        if self.game_type == "nim":
            game = Nim(n=self.config_nim["n"], k=self.config_nim["k"], verbose=self.verbose)
        elif self.game_type == "ledge":
            game = Ledge(self.config_ledge["board_init"], verbose=self.verbose)
        else:
            raise ValueError("Game type is not supported")
        return game

    def get_start_player(self):
        """
        Return the starting player, choosing a random if starting player equals 3.
        :return: int
        """
        player = self.starting_player
        if player == 3:
            player = random.randint(1, 2)
        return player

    @staticmethod
    def get_next_player(player):
        return 2 if player == 1 else 1

    def simulate(self):
        """
        Run G consecutive games (aka. episodes) of the self.game_type using fixed values for the game parameters:
        N and K for NIM, B_init for Ledge. When the G games have finished, your simulator must summarize the win-loss
        statistics. A typical summary (for G = 50) would be a simple statement such as: Player 1 wins 40 of 50 games
        (80%).
        """
        wins = 0  # Number of times player 1 wins
        for _ in range(self.batch_size):
            game = self.get_new_game()

            # For each game, a new Monte Carlo Search Tree is made
            mcts = MonteCarloSearchTree()

            player = self.get_start_player()
            # While the actual game is not finished
            while not game.is_winning_state():

                # Every time we shall select a new action, we perform M number of simulations
                for _ in range(self.num_sim):
                    # One iteration of Monte Carlo Tree Search consists of four steps
                    # 1. Selection
                    mcts.selection()
                    # 2. Expand selected leaf node
                    mcts.expansion()
                    # 3. Simulation
                    mcts.simulation()
                    # 4. Backward propagation
                    mcts.backward()

                # Now use the search tree to choose next action
                action = None

                # Perform this action, moving the game from state s -> s´
                game.perform_action(player, action)

                # Update player
                player = self.get_next_player(player)

                # Set new root of MCST
                mcts.set_root(None)  # TODO: Insert correct Node

        # Report statistics
        logging.info("Player 1 wins {} of {} games ({}%)".format(wins, self.batch_size, round(wins / self.batch_size)))
