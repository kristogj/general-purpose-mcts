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
        """
        Add child to children if child not in children
        :param node:
        :return:
        """
        for child in self.children:
            if child.state == node.state:
                return
        self.children.append(node)

    def get_children(self):
        return self.children

    def __str__(self):
        return "State: {} Action: {} Win: {} Total: {}".format(self.state, self.action, self.win, self.total)
