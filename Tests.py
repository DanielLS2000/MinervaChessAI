import numpy as np
import tensorflow as tf

def fen_to_tensor(fen):
    bitboard = {
        'P': 0, 'N': 0, 'B': 0, 'R': 0, 'Q': 0, 'K': 0,
        'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0, 'k': 0
    }

    # Separar as partes da FEN
    board_str, turn, castling, en_passant, halfmove, fullmove = fen.split()

    # Converter a parte do tabuleiro
    rank_rows = board_str.split('/')
    for i, row in enumerate(rank_rows):
        file_bit = 7
        for char in row:
            if char.isdigit():
                file_bit -= int(char)
            else:
                piece_bit = 1 << (i * 8 + file_bit)
                bitboard[char] |= piece_bit
                file_bit -= 1

    # Criar tensores NumPy para cada tipo de peça
    white_pieces = np.array([bitboard['P'], bitboard['N'], bitboard['B'], bitboard['R'], bitboard['Q'], bitboard['K']], dtype=np.uint64)
    black_pieces = np.array([bitboard['p'], bitboard['n'], bitboard['b'], bitboard['r'], bitboard['q'], bitboard['k']], dtype=np.uint64)

    # Empilhar os tensores para formar a entrada da rede neural
    input_tensor = np.stack([white_pieces, black_pieces])
    input_tensor = tf.convert_to_tensor(input_tensor)

    return input_tensor


# Exemplo de uso:
fen_example = "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2"
tensor_representation = fen_to_tensor(fen_example)
print(tensor_representation.shape)
