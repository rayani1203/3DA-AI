from .Node import Node
import game.TDA as TDA
from game.Card import Value
import time
import math
from copy import deepcopy

class MCTS:
    def __init__(self, iters, time):
        self.iterLimit = iters
        self.timeLimit = time #seconds

    def search(self, state: TDA, prev: Value):
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

            if unexplored and not thisNode.state.isGambitOver():
                thisCard = unexplored[0]
                newState: TDA = deepcopy(thisNode.state)
                newState.simRound(prev, thisCard)
                newNode = Node(newState, thisNode)
                thisNode.children[thisCard] = newNode
                thisNode = newNode
            
            #Step 3: Simulation
            simState : TDA = deepcopy(thisNode.state)
            while not simState.isGambitOver():
                validCards = simState.AIPlayer.cards
                simCard = validCards[0]
                simState.simRound(prev, simCard)
            
            #Step 4: Backpropagation
            result = simState.getGameScore()
            originalPlayer = root.state.AIPlayer

            while thisNode:
                thisNode.visits += 1
                thisNode.totalScore += result
                thisNode = thisNode.parent

        return max(root.children, key=lambda card: 
                   (root.children[card].totalScore / root.children[card].visits) 
                   + math.sqrt(math.log(1 + root.visits) / (1 + root.children[card].visits)))