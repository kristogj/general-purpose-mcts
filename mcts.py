from state_manager import StateManager


class Node:

    def __init__(self, state, player):
        self.state = state
        self.player = player
        self.children = []
        self.win = 0
        self.total = 0

    def increase_win(self):
        self.win += 1

    def increase_total(self):
        self.total += 1

    def add_child(self, node):
        self.children.append(node)

    def get_children(self):
        return self.children


class MonteCarloSearchTree:

    def __init__(self, state):
        self.root = Node(state)
        self.state_manager = StateManager()
        pass

    def set_root(self, node):
        self.root = node

    def selection(self):
        """
        Tree search - Traversing the tree from the root to a leaf node by using the tree policy.
        :return:
        """
        return

    def expansion(self):
        """
        Node Expansion - Generating some or all child states of a parent state, and then connecting the tree node
        housing the parent state (a.k.a. parent node) to the nodes housing the child states (a.k.a. child nodes).
        :return:
        """
        return

    def simulation(self):
        """
        Leaf Evaluation - Estimating the value of a leaf node in the tree by doing a roll-out simulation using the
        default policy from the leaf node’s state to a final state.
        :return:
        """
        return

    def backward(self):
        """
        Backward propagation - Passing the evaluation of a final state back up the tree, updating relevant data
        (see course lecture notes) at all nodes and edges on the path from the final state to the tree root.
        :return:
        """
        return
