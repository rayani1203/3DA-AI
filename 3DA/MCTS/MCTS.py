from .Node import Node
import game.TDA as TDA
from game.Card import Value
import game.Cards as Cards
import time
import math
from copy import deepcopy
import random

class MCTS:
    def __init__(self, iters, time):
        self.iterLimit = iters
        self.timeLimit = time #seconds

    def search(self, state: TDA):
        root = Node(state)

        startTime = time.time()

        for i in range(self.iterLimit):
            print(f"------ iteration {i} --------")
            if time.time() - startTime > self.timeLimit:
                break

            thisNode = root

            #Step 1: Selection
            while thisNode.isFullyExpanded() and thisNode.children:
                print("Selecting best child...\n")
                print()
                print(thisNode.children)
                print()
                thisNode = thisNode.bestChild()
                parent = thisNode.parent
                if parent:
                    for key, child in parent.children.items():
                        if child == thisNode:
                            print(f"This node is a child under the key: {key}\n")
                            break
            
            print("\nAI Player's cards and flight:\n")
            print(thisNode.state.AIPlayer.cards)
            print(thisNode.state.AIPlayer.flight.cards)
            
            #Step 2: Expansion
            if thisNode.state.turn == thisNode.state.numPlayers - 1:
                validCards = thisNode.state.AIPlayer.cards
            else:
                validColors = [color for color in TDA.Color]
                validVals = [num for num in TDA.Value]
                validCards = [Cards.COLOR_TO_CLASS[color](value) for color in validColors for value in validVals]
            unexplored = [card for card in validCards if card not in thisNode.children]

            if unexplored and not thisNode.state.isGambitOver():
                thisCard = random.choice(unexplored)
                print(f"Expanding with card {thisCard.color.value} {thisCard.value.value}")
                newState: TDA = deepcopy(thisNode.state)
                newState.simTurn(thisCard)
                newNode = Node(newState, thisNode)
                thisNode.children[thisCard] = newNode
                thisNode = newNode
            
            #Step 3: Simulation
            simState : TDA = deepcopy(thisNode.state)
            while not simState.isGambitOver():
                validCards = simState.AIPlayer.cards
                simCard = random.choice(validCards)
                simState.simTurn(simCard)
            simState.endGambit()
            
            #Step 4: Backpropagation
            result = simState.getGameScore()
            originalPlayer = root.state.AIPlayer

            while thisNode:
                thisNode.visits += 1
                print(thisNode.totalScore)
                thisNode.totalScore += (result-thisNode.startingPoint)/(thisNode.state.playerGold * thisNode.state.numPlayers)
                print(thisNode.totalScore)
                thisNode = thisNode.parent

        print("------ search complete --------")
        print([(child, root.children[child].totalScore) for child in root.children])
        return max(root.children, key=lambda card: 
                   (root.children[card].totalScore / root.children[card].visits) 
                   + math.sqrt(math.log(1 + root.visits) / (1 + root.children[card].visits)))