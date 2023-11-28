ChessAiv3 = '''
import chess
import chess.polyglot


class ChessAiv3:
    def __init__(self):
        self.polyglot = chess.polyglot.MemoryMappedReader("./books/human.bin")
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

    def evaluate(self, board: chess.Board):
        if board.is_checkmate():
            if board.turn:
                return -999999999
            else:
                return 999999999
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
        color_multiplier = 1 if board.turn else -1

        pawnsq = sum(color_multiplier * self.pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE))
        pawnsq = pawnsq + sum([-self.pawntable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum(color_multiplier * self.knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE))
        knightsq = knightsq + sum(
            [-self.knightstable[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum(color_multiplier * self.bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE))
        bishopsq = bishopsq + sum(
            [-self.bishopstable[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum(color_multiplier * self.rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE))
        rooksq = rooksq + sum([-self.rookstable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum(color_multiplier * self.queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE))
        queensq = queensq + sum(
            [-self.queenstable[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum(color_multiplier * self.kingstable[i] for i in board.pieces(chess.KING, chess.WHITE))
        kingsq = kingsq + sum([-self.kingstable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

        valor = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        if board.turn:
            return valor
        else:
            return -valor

    def negac_star(self, board: chess.Board, depth: int, alpha: int, beta: int, color: int):
        if depth == 0 or board.is_game_over():
            return color * self.evaluate(board)

        legal_moves = list(board.legal_moves)

        for move in legal_moves:
            board.push(move)
            value = -self.negac_star(board, depth - 1, -beta, -alpha, -color)
            board.pop()

            if value > alpha:
                alpha = value
                if alpha >= beta:
                    break

        return alpha

    def negac_star_root(self, board: chess.Board, depth: int):
        best_move = None
        alpha = -9999999999
        beta = 9999999999
        color = 1 if board.turn else -1

        legal_moves = list(board.legal_moves)

        for move in legal_moves:
            board.push(move)
            value = -self.negac_star(board, depth - 1, -beta, -alpha, -color)
            board.pop()

            if value > alpha:
                alpha = value
                best_move = move

        return best_move

    def make_move(self, board: chess.Board, depth: int):
        if board.fullmove_number < 8:
            try:
                move = self.polyglot.weighted_choice(board).move
                return move
            except:
                return self.negac_star_root(board, depth)
        else:
            return self.negac_star_root(board, depth)

    @staticmethod
    def move_random(board):
        legal_moves = list(board.legal_moves)
        if legal_moves:
            return choice(legal_moves)
        else:
            return None
# '''
