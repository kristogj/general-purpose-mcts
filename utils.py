import yaml
import logging


def load_config(path):
    """
    Load config files into a dictionary
    :return: dict
    """
    return yaml.load(open(path, 'r'), Loader=yaml.SafeLoader)


def get_next_player(player):
    return 2 if player == 1 else 1


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
