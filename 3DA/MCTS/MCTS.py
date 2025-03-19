from Node import Node
from game.TDA import TDA
import time

class MCTS:
    def __init__(self, iters, time):
        self.iterLimit = iters
        self.timeLimit = time #seconds

    def search(self, state: TDA):
        root = Node(state)

        startTime = time.time()

        for _ in range(self.iterLimit):
            if time.time() - startTime > self.timeLimit:
                break

            thisNode = root

            #Step 1: Selection
            while thisNode.isFullyExpanded() and thisNode.children:
                thisNode = thisNode.bestChild()
            
            #Step 2: Expansion
            validCards = thisNode.state.AIPlayer.cards
            unexplored = [card for card in validCards if card not in thisNode.children]

            if unexplored:
                thisCard = unexplored[0]
                newState = thisNode.state.copy()
                
