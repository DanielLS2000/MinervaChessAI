ChessAiv3 = '''
import chess
import chess.polyglot


class ChessAiv3:
    def __init__(self):
        self.polyglot = chess.polyglot.MemoryMappedReader("./books/human.bin")
        self.pawntable = [
             0,  0,  0,   0,   0,   0,  0,  0,
             5, 10, 10, -20, -20,  10, 10,  5,
             5, -5, -10,  0,   0, -10, -5,  5,
             0,  0,   0, 20,  20,   0,  0,  0,
             5,  5,  10, 25,  25,  10,  5,  5,
            10, 10,  20, 30,  30,  20, 10, 10,
            50, 50,  50, 50,  50,  50, 50, 50,
             0,  0,   0,  0,   0,   0,  0,  0]

        self.knightstable = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20,   0,   5,   5,   0, -20, -40,
            -30,   5,  10,  15,  15,  10,   5, -30,
            -30,   0,  15,  20,  20,  15,   0, -30,
            -30,   5,  15,  20,  20,  15,   5, -30,
            -30,   0,  10,  15,  15,  10,   0, -30,
            -40, -20,   0,   0,   0,   0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50]
        self.bishopstable = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10,   5,   0,   0,   0,   0,   5, -10,
            -10,  10,  10,  10,  10,  10,  10, -10,
            -10,   0,  10,  10,  10,  10,   0, -10,
            -10,   5,   5,  10,  10,   5,   5, -10,
            -10,   0,   5,  10,  10,   5,   0, -10,
            -10,   0,   0,   0,   0,   0,   0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20]
        self.rookstable = [
             0,  0,  5,  5,  5,  5,  0,  0,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
             5, 10, 10, 10, 10, 10, 10,  5,
             0,  0,  0,  0,  0,  0,  0,  0]
        self.queenstable = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10,   0,   0,  0,  0,   0,   0, -10,
            -10,   5,   5,  5,  5,   5,   0, -10,
              0,   0,   5,  5,  5,   5,   0, - 5,
            - 5,   0,   5,  5,  5,   5,   0, - 5,
            -10,   0,   5,  5,  5,   5,   0, -10,
            -10,   0,   0,  0,  0,   0,   0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20]
        self.kingstable = [
             20,  30,  10,   0,   0,  10,  30,  20,
             20,  20,   0,   0,   0,   0,  20,  20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30]

    def evaluate(self, board: chess.Board) -> int:
        if board.is_checkmate():
            if board.turn:
                return -999999999
            else:
                return 999999999
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0

        wp_map = board.pieces(chess.PAWN, chess.WHITE)
        bp_map = board.pieces(chess.PAWN, chess.BLACK)
        wn_map = board.pieces(chess.KNIGHT, chess.WHITE)
        bn_map = board.pieces(chess.KNIGHT, chess.BLACK)
        wb_map = board.pieces(chess.BISHOP, chess.WHITE)
        bb_map = board.pieces(chess.BISHOP, chess.BLACK)
        wr_map = board.pieces(chess.ROOK, chess.WHITE)
        br_map = board.pieces(chess.ROOK, chess.BLACK)
        wq_map = board.pieces(chess.QUEEN, chess.WHITE)
        bq_map = board.pieces(chess.QUEEN, chess.BLACK)

        wp = len(wp_map)
        bp = len(bp_map)
        wn = len(wn_map)
        bn = len(bn_map)
        wb = len(wb_map)
        bb = len(bb_map)
        wr = len(wr_map)
        br = len(br_map)
        wq = len(wq_map)
        bq = len(bq_map)

        material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

        pawn_score = sum(self.pawntable[i] for i in wp_map)
        pawn_score += sum([-self.pawntable[chess.square_mirror(i)] for i in bp_map])

        knight_score = sum(self.knightstable[i] for i in wn_map)
        knight_score += sum([-self.knightstable[chess.square_mirror(i)] for i in bn_map])

        bishop_score = sum(self.bishopstable[i] for i in wb_map)
        bishop_score += sum([-self.bishopstable[chess.square_mirror(i)] for i in bb_map])

        rook_score = sum(self.rookstable[i] for i in wr_map)
        rook_score += sum([-self.rookstable[chess.square_mirror(i)] for i in br_map])

        queen_score = sum(self.queenstable[i] for i in wq_map)
        queen_score += sum([-self.queenstable[chess.square_mirror(i)] for i in bq_map])

        king_score = sum(self.kingstable[i] for i in board.pieces(chess.KING, chess.WHITE))
        king_score += sum([-self.kingstable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

        valor = material + pawn_score + knight_score + bishop_score + rook_score + queen_score + king_score
        return valor

    def negac_star(self, board: chess.Board, depth: int, alpha: int, beta: int, color: int) -> int:
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

    def negac_star_root(self, board: chess.Board, depth: int) -> chess.Move:
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

    def make_move(self, board: chess.Board, depth: int) -> chess.Move:
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
'''
