import chess

# Define the point values of the pieces
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}


print("================================")
print("\t8  ♜  ♞  ♝  ♛  ♚  ♝  ♞  ♜")
print("\t7  ♟  ♟  ♟  ♟  ♟  ♟  ♟  ♟")
print("\t6  ·  ·  ·  ·  ·  ·  ·  · ")
print("\t5  ·  ·  ·  ·  ·  ·  ·  · ")
print("\t4  ·  ·  ·  ·  ·  ·  ·  · ")
print("\t3  ·  ·  ·  ·  ·  ·  ·  · ")
print("\t2  ♙  ♙  ♙  ♙  ♙  ♙  ♙  ♙")
print("\t1  ♖  ♘  ♗  ♕  ♔  ♗  ♘  ♖")
print("\t   a  b  c  d  e  f  g  h")
print("=================================")

def evaluate_board(board):
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            val = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                score += val
            else:
                score -= val
    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_score = -float("inf")
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_score
    else:
        min_score = float("inf")
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_score = min(min_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_score

def get_ai_move(board):
    best_score = -float("inf")
    best_move = None
    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, 2, -float("inf"), float("inf"), False)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

board = chess.Board()

while not board.is_game_over():
    print(board)
    if board.turn == chess.WHITE:
        try:
            move_str = input("Enter a move in coordinate notation (e.g. 'b1c3'): ")
            move = chess.Move.from_uci(move_str)
            board.push(move)
        except ValueError:
          print("Invalid move, try again.")
    else:
        ai_move = get_ai_move(board)
        board.push(ai_move)
        print("AI move:", ai_move)
    print("--------------------------")
