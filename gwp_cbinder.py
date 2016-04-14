from collections import defaultdict


class Node:
    def __init__(self, value, controller):
        self.controller = controller
        self.value = value
        self.minChild = None

        isEndnode = value == 0
        self.minDepth = 0 if isEndnode else None
        self.calculated = isEndnode

        # valid when there's a mint smaller than the amount
        self.valid = value >= min(controller.mints) or isEndnode

        # print("Node created with value", value)

    def calculateMinDepth(self):
        # print("calculateMinDepth for Node with value", self.value)

        allNodes = (self.controller.getNode(self.value - mint) for mint in self.controller.getMints() if mint <= self.value)
        validNodesWithDepth = [nwd for nwd in [(node, node.getMinDepth()) for node in allNodes if node.valid] if nwd[0].valid]

        if not any(node[0].valid for node in validNodesWithDepth):
            self.valid = False
            self.calculated = True
            return None

        nodeWithMinDepth = min(validNodesWithDepth, key=lambda nwd: nwd[1])
        self.minDepth = nodeWithMinDepth[1]
        self.minChild = nodeWithMinDepth[0]


        self.calculated = True
        return self.minDepth

    def getMinDepth(self):
        return self.minDepth if self.calculated else self.calculateMinDepth()

class Controller:
    def __init__(self, mints):
        self.mints = mints
        self.nodes = dict()

    def run(self, amount):
        endNode = self.getNode(0)

        node = self.getNode(amount)
        depth = node.getMinDepth()

        print("========")

        print("Min Depth:", depth)

        for validNode in sorted((node for node in self.nodes.values() if node.valid), key=lambda node: node.value, reverse=True):
            print("Node with value", validNode.value)

        print("========== Iteration:")
        while node is not None:
            print("Node", node.value)
            node = node.minChild




    def __createNode(self, value):
        self.nodes[value] = Node(value, self)
        return self.nodes[value]

    def getNode(self, value):
        return self.nodes[value] if value in self.nodes.keys() else self.__createNode(value)

    def getMints(self):
        return self.mints


c = Controller([3,5])
c.run(11)