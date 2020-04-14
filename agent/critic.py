from collections import defaultdict
from numpy import log, sqrt


class Critic:

    @staticmethod
    def get_augmented_value(node):
        # TODO: Implement this exploration constant, and check the calculations
        c = sqrt(2)
        return (node.win / node.total) + c * sqrt(log(node.total) / node.win)

    @staticmethod
    def get_augmented_values(nodes):
        return [(node, Critic.get_augmented_value(node)) for node in nodes]
