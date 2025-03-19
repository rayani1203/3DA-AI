from game.TDA import TDA
import math

class Node:
    def __init__(self, state: TDA, parent: 'Node' = None):
        self.state = state  # Game state (3DA)
        self.parent = parent  # Parent Node
        self.children = {}  # Map of move -> child node
        self.visits = 0  # Number of times this node was visited
        self.totalScore = 0  # Number of wins from this node

    def isFullyExpanded(self):
        """Returns True if all possible moves have been explored."""
        return len(self.children) == len(self.state.AIPlayer.cards) or self.state.isGambitOver()

    def bestChild(self, exploration_weight=1.4):
        """Selects the best child using UCB1, handling unvisited nodes properly."""
        for child in self.children.values():
            if child.visits == 0:  
                return child  # Always explore unvisited nodes first

        # Apply UCB1 formula with handling for 0 visits
        return max(self.children.values(), key=lambda node: 
            (node.totalScore / node.visits) + exploration_weight * math.sqrt(math.log(1 + self.visits) / (1 + node.visits)))
