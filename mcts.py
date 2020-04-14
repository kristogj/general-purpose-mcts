from state_manager import StateManager
from critic import Critic
import operator
from utils import get_next_player
import random


class Node:

    def __init__(self, state, action):
        self.state = state
        self.player = None
        self.action = action
        self.parent = None
        self.children = []

        # Values that get updated through backward propagation of the MCTS
        self.win = 0
        self.total = 0

    def increase_win(self):
        self.win += 1

    def increase_total(self):
        self.total += 1

    def set_parent(self, node):
        self.parent = node

    def set_action(self, action):
        self.action = action

    def add_child(self, node):
        self.children.append(node)

    def get_children(self):
        return self.children


class MonteCarloSearchTree:

    def __init__(self, game_type, game_config):
        self.state_manager = StateManager(game_type, game_config)
        self.root = None
        self.critic = Critic()

    def set_root(self, node):
        self.root = node

    def select(self, root=None):
        if not root:
            root = self.root

        # If node has children, make the best choice based on the critic
        children = self.critic.get_augmented_values(root.children)

        # Maximise for P1 and minimize for P2
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
            root = self.select(root=root)

        return root

    def expansion(self, leaf):
        """
        Node Expansion - Generating some or all child states of a parent state, and then connecting the tree node
        housing the parent state (a.k.a. parent node) to the nodes housing the child states (a.k.a. child nodes).
        :return:
        """
        if self.state_manager.is_winning_state(leaf.state):
            # TODO: Check if this is the correct way to handle leaf is winning state
            return leaf

        # Get all legal child states from leaf state
        children_states = self.state_manager.get_child_states(leaf.state)
        children = [Node(state, action) for state, action in children_states]

        # Set leaf as their parent node
        child_player = get_next_player(leaf.player)
        for child in children:
            child.player = child_player
            child.parent = leaf

        # Tree is now expanded, now choose one of the children at random
        return random.choice(children)

    def simulation(self, node):
        """
        Leaf Evaluation - Estimating the value of a leaf node in the tree by doing a roll-out simulation using the
        default policy from the leaf node’s state to a final state.
        :return: int - The player who won the simulated game
        """
        current_node = node
        player = node.player
        while not self.state_manager.is_winning_state(node.state):
            children_states = self.state_manager.get_child_states(current_node.state)
            # Use the default policy (random) to select a child
            current_node = random.choice(children_states)
            get_next_player(player)
        return player

    def backward(self, sim_node, winner):
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
