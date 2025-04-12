import game.TDA as TDA
import math
import random

class Node:
    def __init__(self, state: TDA, parent: 'Node' = None):
        self.state = state  # Game state (3DA)
        self.parent = parent  # Parent Node
        self.children = {}  # Map of move -> child node
        self.visits = 0  # Number of times this node was visited
        self.totalScore = 0  # Number of wins from this node
        self.startingPoint = state.getGameScore()
        self.isAI = state.turn == state.numPlayers - 1

    def isFullyExpanded(self):
        """Returns True if all possible moves have been explored."""
        if self.state.turn == self.state.numPlayers - 1:
            return len(self.children) == len(self.state.AIPlayer.cards) or self.state.isGambitOver()
        else:
            return len(self.children) == (len(TDA.Color)) or self.state.isGambitOver()

    def bestChild(self, exploration_weight=(3)):
        exploration_weight = exploration_weight - 0.2*len(self.state.AIPlayer.flight.cards)
        """Selects the best child using UCB1, handling unvisited nodes properly."""
        valid_children = [child for child in self.children.values() if self.isAI]
        if not valid_children:
            return random.choice(list(self.children.values()))
        for child in valid_children:
            if child.visits == 0:  
                return child  # Always explore unvisited nodes first

        # Apply UCB1 formula with handling for 0 visits
        print("Child scores:")
        for node in valid_children:
            print(node.totalScore / node.visits)
        return max(valid_children, key=lambda node: 
            (node.totalScore / node.visits) + exploration_weight * math.sqrt(math.log(1 + self.visits) / (1 + node.visits)))
