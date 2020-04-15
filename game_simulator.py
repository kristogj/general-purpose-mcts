import logging
from mcts import MonteCarloSearchTree
from tree_node import Node
import random
from utils import get_next_player, get_new_game


class GameSimulator:
    """
    The simulator must provide these results:
        Play-by-Play game action when in verbose mode
        Essential win statistics (for at least one of the two players) for a batch of games.
    """

    def __init__(self, config):
        """
        Config consists of attributes used in the Game Simulator:
            "game_type" - Which game should be played
            "episodes" - Number of "actual" games to be played
            "starting_player" - 1 (Player 1), 2 (Player 2), 3 (Random Player)
            "num_sim" - Number of simulations done in the MCTS before every action taken in a game
            "verbose" - Should every action in the actual games be printed
            "Game" - game specific configurations
        :param config: dict
        """
        logging.info("Initializing GameSimulator")
        self.game_type = config["game_type"]
        self.episodes = config["episodes"]
        self.starting_player = config["starting_player"]
        self.num_sim = config["num_sim"]
        self.verbose = config["verbose"]

        # Game configs
        self.game_config = config["Game"]

    def get_start_player(self):
        """
        Return the starting player, choosing a random if starting player equals 3.
        :return: int
        """
        player = self.starting_player
        if player == 3:
            player = random.randint(1, 2)
        return player

    def simulate(self):
        """
        Run G consecutive games (aka. episodes) of the self.game_type using fixed values for the game parameters:
        N and K for NIM, B_init for Ledge. When the G games have finished, your simulator must summarize the win-loss
        statistics. A typical summary (for G = 50) would be a simple statement such as: Player 1 wins 40 of 50 games
        (80%).
        """
        wins = 0  # Number of times player 1 wins

        # Actual games being played
        for _ in range(self.episodes):
            # The actual game being played this episode
            game = get_new_game(self.game_type, self.game_config, verbose=self.verbose)

            # For each game, a new Monte Carlo Search Tree is made
            mcts = MonteCarloSearchTree(self.game_type, self.game_config)
            state, player = game.get_current_state(), self.get_start_player()
            mcts.set_root(Node(state, None))

            # While the actual game is not finished
            while not game.is_winning_state():

                # Every time we shall select a new action, we perform M number of simulations in MCTS
                for _ in range(self.num_sim):
                    # One iteration of Monte Carlo Tree Search consists of four steps
                    # 1. Selection
                    leaf = mcts.selection()
                    # 2. Expand selected leaf node
                    sim_node = mcts.expansion(leaf)
                    # 3. Simulation
                    winner = mcts.simulation(sim_node)
                    # 4. Backward propagation
                    mcts.backward(sim_node, winner)

                # Now use the search tree to choose next action
                new_root = mcts.select()

                # Perform this action, moving the game from state s -> s´
                game.perform_action(player, new_root.action)

                # Update player
                player = get_next_player(player)

                # Set new root of MCST
                mcts.set_root(new_root)

            # If next player is 2, this means that we are in a winning state, and the next turn was suppose to be
            # for Player 2 which implies that Player 1 did the last action moving it to a winning state.
            if player == 2:
                wins += 1

        # Report statistics
        logging.info("Player1 wins {} of {} games ({}%)".format(wins, self.episodes, round(100*(wins / self.episodes))))
