import argparse
from itertools import groupby


class Node:
    def __init__(self, value, controller):
        self.controller = controller
        self.value = value
        self.minChild = None

        self.isEndnode = value == 0
        self.minDepth = 0 if self.isEndnode else None
        self.calculated = self.isEndnode

        # valid when there's a mint smaller than the amount
        self.valid = value >= min(controller.mints) or self.isEndnode

    def calculateMinDepth(self):
        allNodes = (self.controller.getNode(self.value - mint) for mint in self.controller.getMints() if mint <= self.value)
        validNodesWithDepth = [nwd for nwd in [(node, node.getMinDepth()) for node in allNodes if node.valid] if nwd[0].valid]

        if not any(node[0].valid for node in validNodesWithDepth):
            self.valid = False
            self.calculated = True
            return None

        nodeWithMinDepth = min(validNodesWithDepth, key=lambda nwd: nwd[1])
        self.minDepth = nodeWithMinDepth[1] + 1
        self.minChild = nodeWithMinDepth[0]

        self.calculated = True
        return self.minDepth

    def getMinDepth(self):
        return self.minDepth if self.calculated else self.calculateMinDepth()

class Controller:
    def __init__(self, mints):
        self.mints = sorted([int(mint * 1000) for mint in mints], reverse=True)
        self.nodes = dict()

    def run(self, amount):
        self.getNode(0) # create end-node
        node = self.getNode(int(amount * 1000))
        depth = node.getMinDepth() # do the calculation

        valueslist = list()
        while node is not None and node:
            valueslist.append(node.value)
            node = node.minChild

        changeCoins = sorted([orig-shifted for orig, shifted in zip(valueslist[:-1], valueslist[1:])])

        assert depth == len(changeCoins)

        for coin, group in groupby(changeCoins):
            print("%i x %.2f coin" % (len(list(group)), coin / 1000))
        print("Total coins needed: ", depth)

    def __createNode(self, value):
        self.nodes[value] = Node(value, self)
        return self.nodes[value]

    def getNode(self, value):
        return self.nodes[value] if value in self.nodes.keys() else self.__createNode(value)

    def getMints(self):
        return self.mints


parser = argparse.ArgumentParser(description='Change coin problem')
parser.add_argument("-a", required=True, dest="amount", type=float, help="The amount of change")
parser.add_argument('-c', dest="coins", type=float, nargs='+', default=[0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2],
                    help="The coins")
args = parser.parse_args()

c = Controller(args.coins)
c.run(args.amount)