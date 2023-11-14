import random
import chess


class ChessAi:
    def __init__(self, color: bool):
        self.color = color
        self.pawntable = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.knightstable = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50]
        self.bishopstable = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20]
        self.rookstable = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]
        self.queenstable = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 5, 5, 5, 5, 5, 0, -10,
            0, 0, 5, 5, 5, 5, 0, -5,
            -5, 0, 5, 5, 5, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20]
        self.kingstable = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30]

    def evaluate(self, board):
        if board.is_checkmate():
            if board.turn == self.color:
                return float('-inf')
            else:
                return float('inf')
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0

        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))

        material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
        pawnsq = sum([self.pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq = pawnsq + sum([-self.pawntable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([self.knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum(
            [-self.knightstable[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([self.bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum(
            [-self.bishopstable[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([self.rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-self.rookstable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([self.queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum(
            [-self.queenstable[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([self.kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-self.kingstable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

        valor = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        if board.turn:
            return valor
        else:
            return -valor

    def minimax(self, board, depth: int, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or board.is_checkmate():
            return self.evaluate(board)

        if board.turn:
            maxValue = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                valor = self.minimax(board, depth - 1, alpha, beta)
                board.pop()
                maxValue = max(maxValue, valor)

                alpha = max(alpha, valor)
                if beta <= alpha:
                    break
            return maxValue
        else:
            minValue = float('inf')
            for move in board.legal_moves:
                board.push(move)
                valor = self.minimax(board, depth - 1, alpha, beta)
                board.pop()
                minValue = min(minValue, valor)
                beta = min(beta, valor)
                if beta <= alpha:
                    break
            return minValue

    def make_move(self, board, depth):
        best_move = chess.Move.null()
        best_value = float('-inf')
        if self.color != board.turn:
            for move in board.legal_moves:
                # print(f"Evaluating move {move} as { 'white'if board.turn == True else 'black'}, from {board.legal_moves}")
                board.push(move)
                board_value = self.minimax(board, depth - 1)
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
                board.pop()
            return best_move
        else:
            for move in board.legal_moves:
                board.push(move)
                board_value = -self.minimax(board, depth - 1)
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
                board.pop()
            return best_move

    def move_random(self, board):
        legal_moves = list(board.legal_moves)
        if legal_moves:
            return random.choice(legal_moves)
        else:
            return None
