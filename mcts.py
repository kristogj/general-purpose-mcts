from state_manager import StateManager
import operator
from utils import get_next_player
import random
from numpy import log, sqrt


class MonteCarloSearchTree:

    def __init__(self, game_type, game_config):
        self.state_manager = StateManager(game_type, game_config)
        self.root = None
        self.c = game_config["c"]  # Exploration constant

        self.state_manager.init_new_game()

    def set_root(self, node):
        self.root = node

    def get_augmented_value(self, node, player):
        """
        Calculation needed in order to perform the Tree Policy
        :param node: Node
        :param player: int
        :return: float
        """
        c = self.c if player == 1 else -self.c
        return (node.win / (1 + node.total)) + c * sqrt(log(node.parent.total) / (1 + node.total))

    def select(self, root=None):
        """
        Calculate the the augmented value for each child, and select the best path for the current player to take.
        :param root: Node
        :return:
        """
        if not root:
            root = self.root

        # Calculate the augmented values needed for the tree policy
        children = [(node, self.get_augmented_value(node, root.player)) for node in root.children]

        # Tree Policy = Maximise for P1 and minimize for P2
        if root.player == 1:
            root, value = max(children, key=operator.itemgetter(1))
        else:
            root, value = min(children, key=operator.itemgetter(1))
        return root

    def selection(self):
        """
        Tree search - Traversing the tree from the root to a leaf node by using the tree policy.
        :return: Node
        """
        root = self.root
        children = root.get_children()

        # While root is not a leaf node
        while len(children) != 0:
            root = self.select(root)
            children = root.get_children()

        return root

    def expansion(self, leaf):
        """
        Node Expansion - Generating some or all child states of a parent state, and then connecting the tree node
        housing the parent state (a.k.a. parent node) to the nodes housing the child states (a.k.a. child nodes).
        :return:
        """
        if self.state_manager.is_winning_state(leaf.state):
            return leaf

        # Get all legal child states from leaf state
        leaf.children = self.state_manager.get_child_nodes(leaf.state)

        # Set leaf as their parent node
        child_player = get_next_player(leaf.player)
        for child in leaf.children:
            child.player = child_player
            child.parent = leaf
        # Tree is now expanded, return one of them at random
        return random.choice(leaf.children)

    def simulation(self, node):
        """
        Leaf Evaluation - Estimating the value of a leaf node in the tree by doing a roll-out simulation using the
        default policy from the leaf node’s state to a final state.
        :return: int - The player who won the simulated game
        """
        current_node = node
        children = self.state_manager.get_child_nodes(current_node.state)
        player = get_next_player(node.player)
        while len(children) != 0:
            # Use the default policy (random) to select a child
            current_node = random.choice(children)
            player = get_next_player(player)
            children = self.state_manager.get_child_nodes(current_node.state)
        return player

    @staticmethod
    def backward(sim_node, winner):
        """
        Backward propagation - Passing the evaluation of a final state back up the tree, updating relevant data
        (see course lecture notes) at all nodes and edges on the path from the final state to the tree root.
        :param sim_node: Node - leaf node to go backward from
        :param winner: int - player who won the simulated game
        :return: None
        """
        node = sim_node
        while node:
            if node.player == winner:
                node.increase_win()
            node.increase_total()
            node = node.parent
