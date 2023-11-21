import chess
import chess.pgn
import chess.engine
import time
import os
from ChessAi import ChessAi
from ChessAi002 import ChessAi002


def against_human(cor):
    time_player = True if cor == "True" else False
    ai = ChessAi(not time_player)

    game_start = time.time_ns()
    count = 0
    movehistory = []
    game = chess.pgn.Game()
    board = chess.Board()
    print(board)
    while not board.is_game_over():
        if board.turn:
            count += 1
            print(f'\n{count}]\n')
            print("---- white turn -----\n")
            if time_player:
                move = input("Insira seu movimento(san): ")
                movehistory.append(move)
                board.push_san(move)
                print(board)
            else:
                move = ai.make_move(board, 3)
                movehistory.append(move)
                print(f"move: {move}")
                board.push(move)
                print(board)
        else:
            print("---- black turn -----\n")
            if not time_player:
                move = input("Insira seu movimento(san): ")
                movehistory.append(move)
                board.push_san(move)
                print(board)
            else:
                move = ai.make_move(board, 3)
                movehistory.append(move)
                print(f"move: {move}")
                board.push(move)
                print(board)

    game_finish = time.time_ns()
    game.add_line(movehistory)
    game.headers["Result"] = str(board.result())
    game.headers["Round"] = str(count)
    game.headers["White"] = "Player" if bool(cor) else "ChessAI"
    game.headers["Black"] = "ChessAI" if bool(cor) else "Player"
    print(game)
    print(board.outcome())
    print(str((game_finish - game_start) / 1000000) + "ms")
    x = input("press any button to continue")


def against_itself(qnt, show):
    qnt = int(qnt)
    show = True if show == "y" else False

    ai_white = ChessAi(True)
    ai_black = ChessAi002(False)

    match_history = {
        "White": 0,
        "Black": 0,
        "Draw": 0
    }

    for i in range(qnt):
        game_start = time.time_ns()
        movehistory = []
        board = chess.Board()
        if show:
            print(board)
        count = 0

        print(f"Match {i}")
        while not board.is_game_over():
            if board.turn:
                count += 1
                if show:
                    print(f'\n{count}]\n')
                move = ai_white.make_move(board, 3)
                movehistory.append(move)
                board.push(move)
                if show:
                    print("---- white turn(MiniMax) -----\n")
                    print(f"move: {move}")
                    print(board)
            else:

                move = ai_black.negac_star_root(board, 3)
                movehistory.append(move)
                board.push(move)
                if show:
                    print("---- black turn(NegaC) -----\n")
                    print(f"move: {move}")
                    print(board)

        game_finish = time.time_ns()
        print(board.outcome().winner)
        if board.outcome().winner:
            match_history["White"] += 1
        elif board.outcome().winner == False:
            match_history["Black"] += 1
        else:
            match_history["Draw"] += 1
        print(f"{i}º game time: " + str((game_finish - game_start) / 1000000) + "ms")
        print(f"rounds {count}")

    print(f"White wins: {match_history['White']}\n"
          f"Black wins: {match_history['Black']}\n"
          f"Draws: {match_history['Draw']}\n")
    x = input("press any button to continue")


def against_stockfish(qnt, show):
    qnt = int(qnt)
    show = True if show == "y" else False

    ai_white = ChessAi(True)
    engineStockFish = chess.engine.SimpleEngine.popen_uci("./OtherEngines/stockfish/stockfish.exe")

    match_history = {
        "White": 0,
        "Black": 0,
        "Draw": 0
    }

    for i in range(qnt):
        game_start = time.time_ns()
        movehistory = []
        board = chess.Board()
        if show:
            print(board)
        count = 0

        print(f"Match {i}")
        while not board.is_game_over():
            if board.turn:
                count += 1
                if show:
                    print(f'\n{count}]\n')
                move = ai_white.make_move(board, 3)
                movehistory.append(move)
                board.push(move)
                if show:
                    print("---- white turn -----\n")
                    print(f"move: {move}")
                    print(board)
            else:

                move = engineStockFish.play(board, chess.engine.Limit(time=0.1))
                movehistory.append(move.move)
                board.push(move.move)
                if show:
                    print("---- black turn -----\n")
                    print(f"move: {move.move}")
                    print(board)

        game_finish = time.time_ns()
        print(board.outcome().winner)
        if board.outcome().winner:
            match_history["White"] += 1
        elif board.outcome().winner == False:
            match_history["Black"] += 1
        else:
            match_history["Draw"] += 1
        print(f"{i}º game time: " + str((game_finish - game_start) / 1000000) + "ms")
        print(f"rounds {count}")

    print(f"ChessAI White wins: {match_history['White']}\n"
          f"StockFish wins: {match_history['Black']}\n"
          f"Draws: {match_history['Draw']}\n")
    x = input("press any button to continue")


def main_menu():
    os.system('cls')
    print('''
---   AI Xeque-Mate   ---
--- Programa de Testes ---

1 - Teste contra humano
2 - Teste contra outra versão
3 - Teste contra Stockfish
''')
    modo = input("Insira o modo: ")
    if modo == '1':
        cor = input("Quer usar as peças brancas(True) ou pretas(False)?: ")
        against_human(cor)
    elif modo == '2':
        qnt = input("Quantas partidas serão jogadas?: ")
        show = input("Deseja ver a execução das partidas?(y/n): ")
        against_itself(qnt, show)
    elif modo == '3':
        qnt = input("Quantas partidas serão jogadas?: ")
        show = input("Deseja ver a execução das partidas?(y/n): ")
        against_stockfish(qnt, show)


if __name__ == '__main__':
    while True:
        main_menu()
