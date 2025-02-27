import random

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9  # 3x3 board stored as a list
        self.current_player = 'O'

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
    
    def copy(self):
        new_game = TicTacToe()
        new_game.board = self.board[:]  # ✅ Properly copies the list
        new_game.current_player = self.current_player
        return new_game

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

    def best_child(self, exploration_weight=1.4):
        """Selects the best child using UCB1, handling unvisited nodes properly."""
        for child in self.children.values():
            if child.visits == 0:  
                return child  # Always explore unvisited nodes first

        # Apply UCB1 formula with handling for 0 visits
        return max(self.children.values(), key=lambda node: 
            (node.wins / node.visits) + exploration_weight * math.sqrt(math.log(1 + self.visits) / (1 + node.visits)))

        
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

            # Step 1: Selection - Follow the best child until a non-fully expanded node is found
            while node.is_fully_expanded() and node.children:
                node = node.best_child()

            # Step 2: Expansion - Add one new move to the tree
            valid_moves = node.state.get_valid_moves()
            unexplored_moves = [m for m in valid_moves if m not in node.children]

            if unexplored_moves:  # Expand only if there's an unexplored move
                move = random.choice(unexplored_moves)  # Pick one move to expand
                new_state = node.state.copy()  # Properly copy the game state
                new_state.make_move(move)  # Apply move
                new_node = Node(new_state, node)  # Create new node
                node.children[move] = new_node  # Add to tree
                node = new_node  # Move into expanded node (but don't immediately select best child)


            # Step 3: Simulation (Rollout)
            sim_state = node.state.copy()
            sim_state.current_player = node.state.current_player
            while sim_state.check_winner() is None:
                heuristic = heuristic_move(sim_state)
                if heuristic:
                    sim_state.make_move(heuristic)  # ✅ Use a heuristic if available
                else:
                    sim_state.make_move(random.choice(sim_state.get_valid_moves()))  # ✅ Use random move

            # Step 4: Backpropagation
            result = sim_state.check_winner()
            original_player = root.state.current_player  # Store the AI's original turn

            while node:
                node.visits += 1
                if result == original_player:  # ✅ AI wins
                    node.wins += 1
                elif result == 'D':  # ✅ Draw counts as partial win
                    node.wins += 0.5
                else:  # ✅ AI loses
                    node.wins -= 0.5
                node = node.parent


        # Select the best move
        return max(root.children, key=lambda move: 
            root.children[move].wins / root.children[move].visits + 
            math.sqrt(math.log(1 + root.visits) / (1 + root.children[move].visits))
        )


def heuristic_move(game):
    """Returns a move if an immediate win or block is possible."""
    current_player = game.current_player
    opponent = 'O' if current_player == 'X' else 'X'

    # 1️⃣ Check if we can win immediately
    for move in game.get_valid_moves():
        temp_game = game.copy()
        temp_game.make_move(move)
        if temp_game.check_winner() == current_player:
            return move

    # 2️⃣ Check if the opponent can win on their next move, and block it
    for move in game.get_valid_moves():
        temp_game = game.copy()
        temp_game.current_player = opponent  # Simulate opponent's turn
        temp_game.make_move(move)
        if temp_game.check_winner() == opponent:
            return move

    # 3️⃣ No immediate win or block found, return None.
    return None


game = TicTacToe()
mcts = MCTS(iter_limit=5000, time_limit=5.0)
mcts_tree = {}  # ✅ Store MCTS results between turns

while game.check_winner() is None:
    game.print_board()

    board_state = tuple(game.board)  # ✅ Convert board to immutable tuple for dictionary key

    if game.current_player == 'X':
        heuristic = heuristic_move(game)
        if heuristic:
            move = heuristic
        else:
            if board_state not in mcts_tree:
                mcts_tree[board_state] = Node(game.copy())  # Store a copy of the game state
            move = mcts.search(mcts_tree[board_state].state)  # Retrieve search tree
    else:
        move = int(input())

    game.make_move(move)

game.print_board()
print("Winner:", game.check_winner())
