import yaml
import logging
from game import Nim, Ledge


def load_config(path):
    """
    Load config files into a dictionary
    :return: dict
    """
    return yaml.load(open(path, 'r'), Loader=yaml.SafeLoader)


def get_next_player(player):
    return 2 if player == 1 else 1


def get_new_game(game_type, game_config, verbose):
    if game_type == "nim":
        game = Nim(n=game_config["Nim"]["n"], k=game_config["Nim"]["k"], verbose=verbose)
    elif game_type == "ledge":
        game = Ledge(game_config["Ledge"]["board_init"], verbose=verbose)
    else:
        raise ValueError("Game type is not supported")
    return game


def init_logger():
    """
    Initialize logger settings
    :return: None
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("app.log", mode="w"),
            logging.StreamHandler()
        ])
