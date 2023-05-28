import chess
# BY HARRIS AAMIR 20I0943 SE-S
# Define the point values of the pieces
piece_values = {
    chess.PAWN: 5,
    chess.KNIGHT: 15,
    chess.BISHOP: 15,
    chess.ROOK: 25,
    chess.QUEEN: 50,
    chess.KING: 1
}
#evaluating board on current pieces
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
#printing board with labels and symbols
def printBoard(b):
    strBoard=str(b)
    strBoard=strBoard.replace("p", "♙")
    strBoard=strBoard.replace("r", "♖")
    strBoard=strBoard.replace("n", "♘")
    strBoard=strBoard.replace("b", "♗")
    strBoard=strBoard.replace("q", "♕")
    strBoard=strBoard.replace("k", "♔")
    strBoard=strBoard.replace("P", "♟")
    strBoard=strBoard.replace("R", "♜")
    strBoard=strBoard.replace("N", "♞")
    strBoard=strBoard.replace("B", "♝")
    strBoard=strBoard.replace("Q", "♛")
    strBoard=strBoard.replace("K", "♚")
    print("=====================")
    for i in range(127):
      if i%16==0:
        print(f"{8-int(i/16)}  ",end="")
      print(strBoard[i],end="")
    print("\n   a b c d e f g h")
    print("=====================")

#prunning occurs when beta<alpha
def checkPruning(beta,alpha):
    if beta <= alpha:
        return True
    else: return False 
#minMax algorithm
def minMax(board, depth, alpha, beta, player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if player=="maximizingPlayer":
        maxScore = -1000000
        for move in board.legal_moves:
            board.push(move)
            score = minMax(board, depth - 1, alpha, beta, "minimizingPlayer")
            board.pop()
            maxScore = max(maxScore, score)
            alpha = max(alpha, score)
            if checkPruning(beta,alpha):
                break
        return maxScore
    else:
        minScore = 1000000 #represents pos infinty 
        for move in board.legal_moves:
            board.push(move)
            score = minMax(board, depth - 1, alpha, beta, "maximizingPlayer")
            board.pop()
            minScore = min(minScore, score)
            beta = min(beta, score)
            if checkPruning(beta,alpha):
                break
        return minScore
aiMoves=[]
#generate and check moves for AI
def moveByAI(board):
    bestScore = -1000000 #represents neg infinty 
    bestMove = None 
    # compare every legal move 
    for move in board.legal_moves:
        if move in aiMoves: continue
        board.push(move)
        score = minMax(board, 4, -1000000, 1000000, "minimizingPlayer")
        board.pop()
        if score > bestScore:
            bestScore = score
            bestMove = move
    return bestMove

board = chess.Board()
# main game while loop 
while not board.is_game_over():
    printBoard(board)
    if board.turn == chess.WHITE:  #player turn 
        try:
            moveInput = input("Enter a move in coordinate notation (e.g. 'b1c3'): ")
            userMove = chess.Move.from_uci(moveInput)
            if chess.Move.from_uci(moveInput) in board.legal_moves:
             board.push_uci(moveInput)
            else:
              print("Illegal move. Try again.")
        except ValueError:
          print("Invalid move notaion, try again.")
    else:   #ai turn 
        aiMove = moveByAI(board)
        board.push(aiMove)
        aiMoves.append(aiMove)
        print("Best move selected by PC:", aiMove)
    if board.is_checkmate():
        print("Checkmate! Game over.")
        break
    print("--------------------------")
#check for winner 
printBoard(board)
if board.result() == "1-0":
    print("White wins!")
elif board.result() == "0-1":
    print("Black wins!")
else:
    print("Draw!")