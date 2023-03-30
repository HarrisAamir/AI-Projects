import chess
import random

# Set up the initial chess board
board = chess.Board()

# Define a function to make a random legal move
def make_random_move(board):
    legal_moves = list(board.legal_moves)
    random_move = random.choice(legal_moves)
    board.push(random_move)

# Define a loop to alternate between human and AI moves
while not board.is_game_over():
    print(board)
    if board.turn == chess.WHITE:
        try:
            human_move = input("Enter your move (in algebraic notation): ")
            board.push_san(human_move)
        except ValueError:
          print("Invalid move, try again.")
    else:
        # AI move
        make_random_move(board)
    print("-------------------")
    # Print the current board state
 
