import random

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9  # 3x3 board stored as a list
        self.current_player = 'X'

    def get_valid_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def make_move(self, move):
        """Plays a move and switches players."""
        if self.board[move] == ' ':
            self.board[move] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def undo_move(self, move):
        """Reverts a move (used in simulations)."""
        self.board[move] = ' '
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        """Returns 'X' or 'O' if there's a winner, 'D' for draw, or None if game is ongoing."""
        winning_positions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for (a, b, c) in winning_positions:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != ' ':
                return self.board[a]
        return 'D' if ' ' not in self.board else None  # Draw if no moves left

    def print_board(self):
        """Displays the board."""
        print("\n".join([
            f"{self.board[0]} | {self.board[1]} | {self.board[2]}",
            "--+---+--",
            f"{self.board[3]} | {self.board[4]} | {self.board[5]}",
            "--+---+--",
            f"{self.board[6]} | {self.board[7]} | {self.board[8]}"
        ]))
        print()

import math
import time

class Node:
    def __init__(self, state, parent=None):
        self.state = state  # Game state (TicTacToe)
        self.parent = parent  # Parent Node
        self.children = {}  # Map of move -> child node
        self.visits = 0  # Number of times this node was visited
        self.wins = 0  # Number of wins from this node

    def is_fully_expanded(self):
        """Returns True if all possible moves have been explored."""
        return len(self.children) == len(self.state.get_valid_moves())

    def best_child(self, exploration_weight=1.41):
        """Selects the best child using UCB1 formula."""
        return max(self.children.values(), key=lambda node: 
            (node.wins / node.visits) + exploration_weight * math.sqrt(math.log(self.visits) / node.visits))
        
class MCTS:
    def __init__(self, iter_limit=1000, time_limit=1.0):
        self.iter_limit = iter_limit  # Max number of MCTS iterations
        self.time_limit = time_limit  # Max seconds to run MCTS

    def search(self, state):
        """Runs MCTS and returns the best move."""
        root = Node(state)

        start_time = time.time()
        for _ in range(self.iter_limit):
            if time.time() - start_time > self.time_limit:
                break

            node = root
            # Step 1: Selection
            while node.is_fully_expanded() and node.children:
                node = node.best_child()

            # Step 2: Expansion
            valid_moves = node.state.get_valid_moves()
            if valid_moves:
                move = random.choice(valid_moves)
                new_state = TicTacToe()
                new_state.board = node.state.board[:]  # Copy board
                new_state.current_player = node.state.current_player
                new_state.make_move(move)
                node.children[move] = Node(new_state, node)
                node = node.children[move]

            # Step 3: Simulation (Rollout)
            sim_state = TicTacToe()
            sim_state.board = node.state.board[:]
            sim_state.current_player = node.state.current_player
            while sim_state.check_winner() is None:
                sim_state.make_move(random.choice(sim_state.get_valid_moves()))

            # Step 4: Backpropagation
            result = sim_state.check_winner()
            while node:
                node.visits += 1
                if result == node.state.current_player:  # Reward wins
                    node.wins += 1
                elif result == 'D':  # Draws count as half a win
                    node.wins += 0.5
                node = node.parent

        # Select the best move
        return max(root.children, key=lambda move: root.children[move].visits)
game = TicTacToe()
mcts = MCTS(iter_limit=10000000, time_limit=30.0)

while game.check_winner() is None:
    game.print_board()

    if game.current_player == 'X':
        move = mcts.search(game)
    else:
        move = int(input())

    game.make_move(move)

game.print_board()
print("Winner:", game.check_winner())
