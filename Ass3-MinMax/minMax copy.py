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

def minimax(board, depth, alpha, beta, player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if player=="maximizing_player":
        maxScore = -1000000
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, "minimizing_player")
            board.pop()
            maxScore = max(maxScore, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return maxScore
    else:
        minScore = 1000000 #represents pos infinty 
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, "maximizing_player")
            board.pop()
            minScore = min(minScore, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return minScore
aiMoves=[]
def moveByAI(board):
    bestScore = -1000000 #represents neg infinty 
    bestMove = None 
    # compare every legal move 
    for move in board.legal_moves:
        if move in aiMoves: continue
        board.push(move)
        score = minimax(board, 2, -1000000, 1000000, "minimizing_player")
        board.pop()
        if score > bestScore:
            bestScore = score
            bestMove = move
    return bestMove

board = chess.Board()
print(type(board))
while not board.is_game_over():
    print(board)
    if board.turn == chess.WHITE:
        try:
            moveInput = input("Enter a move in coordinate notation (e.g. 'b1c3'): ")
            userMove = chess.Move.from_uci(moveInput)
            if chess.Move.from_uci(moveInput) in board.legal_moves:
             board.push_uci(moveInput)
            else:
              print("Illegal move. Try again.")
            # board.push(userMove)
        except ValueError:
          print("Invalid move, try again.")
    else:
        pcMove = moveByAI(board)
        board.push(pcMove)
        aiMoves.append(pcMove)
        print("Best move selected by PC:", pcMove)
    print("--------------------------")

print(board)
if board.result() == "1-0":
    print("White wins!")
elif board.result() == "0-1":
    print("Black wins!")
else:
    print("Draw!")


    # strBoard=strBoard.replace("p", "♙")
    # strBoard=strBoard.replace("r", "♖")
    # strBoard=strBoard.replace("n", "♘")
    # strBoard=strBoard.replace("b", "♗")
    # strBoard=strBoard.replace("q", "♕")
    # strBoard=strBoard.replace("k", "♔")

    # strBoard=strBoard.replace("P", "♟")
    # strBoard=strBoard.replace("R", "♜")
    # strBoard=strBoard.replace("N", "♞")
    # strBoard=strBoard.replace("B", "♝")
    # strBoard=strBoard.replace("Q", "♛")
    # strBoard=strBoard.replace("K", "♚")