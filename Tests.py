import chess
import chess.svg
import numpy as np


def fen_to_bitboard(fen):
    board = chess.Board(fen)
    bitboard_list = []
    pieces = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    colors = [chess.WHITE, chess.BLACK]

    # Obter bitboard para cada peça no tabuleiro
    for color in colors:
        for piece in pieces:
            bitboard = board.pieces_mask(piece, color)
            bitboard_string = bin(bitboard)[2:]
            bitboard_string = bitboard_string.zfill(64)
            # Adicionar bitboard da peça atual à lista

            bitboard_list.extend([int(bit) for bit in bitboard_string])
    # Adicionar o bit indicando a cor do jogador atual (0 para preto, 1 para branco)
    bitboard_list.append(int(board.turn))

    chessboard = np.array(bitboard_list, dtype=np.uint64)

    return chessboard

# Empilhar os tensores para formar a entrada da rede neural
    #input_tensor = np.array([bitboard['P'], bitboard['N'], bitboard['B'], bitboard['R'], bitboard['Q'], bitboard['K'],
                         #   bitboard['p'], bitboard['n'], bitboard['b'], bitboard['r'], bitboard['q'], bitboard['k']], dtype=np.uint64)


# Exemplo de uso
fen_notation = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
board = chess.Board(fen_notation)
# bitboard = board.pieces_mask(chess.PAWN, chess.WHITE)
bitboard = fen_to_bitboard(fen_notation)
print(bitboard)
print(len(bitboard))
print(board)

# Função para converter um número inteiro em binário e dividir em uma lista
def int_para_binario_lista(numero):
    # Obtém a representação binária como uma string e remove o prefixo '0b'
    binario_string = bin(numero)[2:]

    # Converte a string binária em uma lista de dígitos
    lista_binaria = [int(digito) for digito in binario_string]

    return lista_binaria

# Exemplo de uso
numero_inteiro = 200
lista_binaria = int_para_binario_lista(numero_inteiro)

print(f"Número inteiro: {numero_inteiro}")
print(f"Representação binária: {lista_binaria}")

