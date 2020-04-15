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
        """
        Node was part of the path to victory - increase win value
        :return:
        """
        self.win += 1

    def increase_total(self):
        """
        Node was on the path taken in the search - increase total
        :return:
        """
        self.total += 1

    def set_parent(self, node):
        """
        Set the parent for this node equal to node
        :param node: Node
        :return:
        """
        self.parent = node

    def set_action(self, action):
        """
        Set the action taken to get to this node
        :param action: Type depends on the game
        :return: None
        """
        self.action = action

    def get_children(self):
        """
        Return the children for this node
        :return: list[Node]
        """
        return self.children

    def __str__(self):
        return "State: {} Action: {} Win: {} Total: {}".format(self.state, self.action, self.win, self.total)
