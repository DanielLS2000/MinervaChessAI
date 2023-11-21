import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QSizePolicy
import chess
import chess.svg
import chess.engine
from io import BytesIO
from PyQt5.QtGui import QPixmap
from ChessAi002 import ChessAi002
from ChessAi import ChessAi
import time
import re


class ChessGameGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.board = chess.Board()
        self.mode = '1'
        self.ai = ChessAi002(False)
        self.initUI()

    def initUI(self):
        # Componentes da interface
        self.image_label = QLabel(self)
        self.player_move_field = QLineEdit(self)
        self.play_button = QPushButton('Jogar', self)
        self.play_button.clicked.connect(self.play_move)

        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red")

        # Layout principal
        main_layout = QHBoxLayout()

        # Layout para a imagem
        chess_layout = QVBoxLayout()
        chess_layout.addWidget(self.image_label)

        # Layout para o input_field
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.player_move_field)
        input_layout.addWidget(self.play_button)
        chess_layout.addLayout(input_layout)

        main_layout.addLayout(chess_layout)

        main_layout.addWidget(self.error_label)

        # Layout para os modos de jogo
        mode_layout = QVBoxLayout()

        # Botão "Jogar contra IA"
        play_vs_ai_button = QPushButton('Jogar contra IA', self)
        play_vs_ai_button.clicked.connect(lambda: self.change_mode('1'))
        mode_layout.addWidget(play_vs_ai_button)

        # Botão "IA vs IA"
        ai_vs_ai_button = QPushButton('IA vs IA', self)
        ai_vs_ai_button.clicked.connect(lambda: self.change_mode('2'))
        mode_layout.addWidget(ai_vs_ai_button)

        # Botão "IA vs StockFish"
        play_vs_stockfish_button = QPushButton('IA vs StockFish', self)
        play_vs_stockfish_button.clicked.connect(lambda: self.change_mode('3'))
        mode_layout.addWidget(play_vs_stockfish_button)

        main_layout.addLayout(mode_layout)

        # Definindo tamanhos relativos
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.player_move_field.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.play_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        play_vs_ai_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        ai_vs_ai_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        play_vs_stockfish_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setLayout(main_layout)
        self.update_board_image()

        # Ajustes da janela
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Chess Game')
        self.show()

    def play_move(self):
        padrao = re.compile(r'^[a-z][0-9][a-z][0-9]$')
        move = self.player_move_field.text()
        if not move:
            self.error_label.setText("Erro: O campo de entrada está vazio.")
            return
        elif not bool(padrao.match(move)):
            self.error_label.setText("Erro: Jogada Invalida.")
            return
        else:
            self.player_move_field.clear()
            move = chess.Move.from_uci(move)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board_image()
                self.ai_play()
                self.error_label.setText(f"Jogada: {move}")
            else:
                self.error_label.setText("Erro: Jogada Invalida.")

    def change_mode(self, mode):
        # Reiniciando Jogo
        self.board = chess.Board()
        self.update_board_image()
        self.mode = mode
        if mode == '1':
            self.player_move_field.setDisabled(False)
            self.play_button.setDisabled(False)
        elif mode == '2':
            self.player_move_field.setDisabled(True)
            self.play_button.setDisabled(True)
            self.ai_game()
        elif mode == '3':
            self.player_move_field.setDisabled(True)
            self.play_button.setDisabled(True)
            self.stockfish_game()

    def update_board_image(self):
        # Implemente a lógica para atualizar a imagem do tabuleiro aqui
        board_svg = chess.svg.board(board=self.board)

        image_bytes = BytesIO(board_svg.encode('utf-8'))
        pixmap = QPixmap()
        pixmap.loadFromData(image_bytes.read())

        self.image_label.setPixmap(pixmap)

    def ai_play(self):
        move = self.ai.negac_star_root(self.board, 3)
        self.board.push(move)

        # Update Board
        self.error_label.setText(f"Jogada: {move}")
        self.update_board_image()


    def ai_game(self, n_games=1):
        ai_white = ChessAi(True)
        ai_black = ChessAi002(False)

        match_history = {
            "White": 0,
            "Black": 0,
            "Draw": 0
        }

        # self.ai_play(ai_white, ai_black)

        for i in range(n_games):
            game_start = time.time_ns()
            movehistory = []
            self.board = chess.Board()
            self.update_board_image()

            while not self.board.is_game_over():
                if self.board.turn:
                    move = ai_white.make_move(self.board, 3)
                    movehistory.append(move)
                    self.board.push(move)

                    # Update board
                    self.update_board_image()
                    QApplication.processEvents()
                else:
                    move = ai_black.negac_star_root(self.board, 3)
                    movehistory.append(move)
                    self.board.push(move)

                    # Update Board
                    self.update_board_image()
                    QApplication.processEvents()

            game_finish = time.time_ns()
            print(self.board.outcome().winner)
            if self.board.outcome().winner:
                match_history["White"] += 1
            elif self.board.outcome().winner == False:
                match_history["Black"] += 1
            else:
                match_history["Draw"] += 1
            print(f"{i}º game time: " + str((game_finish - game_start) / 1000000) + "ms")
            print(f"rounds {self.board.fullmove_number}")

        print(f"White wins: {match_history['White']}\n"
              f"Black wins: {match_history['Black']}\n"
              f"Draws: {match_history['Draw']}\n")

    def stockfish_game(self, n_games=1):
        ai_white = ChessAi002(True)
        engineStockFish = chess.engine.SimpleEngine.popen_uci("./OtherEngines/stockfish/stockfish.exe")

        match_history = {
            "White": 0,
            "Black": 0,
            "Draw": 0
        }

        for i in range(n_games):
            game_start = time.time_ns()
            movehistory = []
            self.board = chess.Board()

            print(f"Match {i}")
            while not self.board.is_game_over():
                if self.board.turn:
                    move = ai_white.negac_star_root(self.board, 3)
                    movehistory.append(move)
                    self.board.push(move)
                    # Update Board
                    self.update_board_image()
                    QApplication.processEvents()
                else:

                    move = engineStockFish.play(self.board, chess.engine.Limit(time=0.1))
                    movehistory.append(move.move)
                    self.board.push(move.move)
                    # Update Board
                    self.update_board_image()
                    QApplication.processEvents()

            game_finish = time.time_ns()
            print(self.board.outcome().winner)
            if self.board.outcome().winner:
                match_history["White"] += 1
            elif self.board.outcome().winner == False:
                match_history["Black"] += 1
            else:
                match_history["Draw"] += 1
            print(f"{i}º game time: " + str((game_finish - game_start) / 1000000) + "ms")
            print(f"rounds {self.board.fullmove_number}")

        print(f"ChessAI White wins: {match_history['White']}\n"
              f"StockFish wins: {match_history['Black']}\n"
              f"Draws: {match_history['Draw']}\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChessGameGUI()
    sys.exit(app.exec_())
