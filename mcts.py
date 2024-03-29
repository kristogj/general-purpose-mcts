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
        return node.value + c * sqrt(log(node.parent.total) / (1 + node.total))

    def select(self, root):
        """
        Calculate the the augmented value for each child, and select the best path for the current player to take.
        :param root: Node
        :return:
        """
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
        # Get all legal child states from leaf state
        leaf.children = self.state_manager.get_child_nodes(leaf.state)

        # Set leaf as their parent node
        child_player = get_next_player(leaf.player)
        for child in leaf.children:
            child.player = child_player
            child.parent = leaf
        # Tree is now expanded, return the leaf, and simulate to game over
        return leaf

    def simulation(self, node):
        """
        Leaf Evaluation - Estimating the value of a leaf node in the tree by doing a roll-out simulation using the
        default policy from the leaf node’s state to a final state.
        :return: int - The player who won the simulated game
        """
        current_node = node
        children = self.state_manager.get_child_nodes(current_node.state)
        player = node.player
        while len(children) != 0:
            # Use the default policy (random) to select a child
            current_node = random.choice(children)
            player = get_next_player(player)
            children = self.state_manager.get_child_nodes(current_node.state)
        winner = get_next_player(player)  # Winner was actually the prev player who made a move
        return int(winner == 1)

    @staticmethod
    def backward(sim_node, z):
        """
        Backward propagation - Passing the evaluation of a final state back up the tree, updating relevant data
        (see course lecture notes) at all nodes and edges on the path from the final state to the tree root.
        :param sim_node: Node - leaf node to go backward from
        :param z: int - 1 if player 1 won, else 0
        :return: None
        """
        node = sim_node
        node.total += 1
        while node.parent:
            node.parent.total += 1
            node.value += (z - node.value) / node.total
            node = node.parent

    def select_actual_action(self, player):
        """
        To select the actual action to take in the game, select the edge with the highest visit count
        :return: Node
        """
        children = [(child, child.value) for child in self.root.children]

        # Tree Policy = Maximise for P1 and minimize for P2
        if player == 1:
            root, value = max(children, key=operator.itemgetter(1))
        else:
            root, value = min(children, key=operator.itemgetter(1))
        return root

    def tree_print(self):
        nodes = [self.root]
        while nodes:
            curr = nodes[0]
            nodes = nodes[1:]
            print((curr.total, curr.player))
            nodes += curr.children
