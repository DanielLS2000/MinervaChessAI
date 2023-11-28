import chess
import chess.polyglot
import chess.engine

ai = chess.engine.SimpleEngine.popen_uci("./OtherEngines/stockfish/stockfish.exe")

board = chess.Board()
info = ai.analyse(board, chess.engine.Limit(time=0.1))
score = info['score']
print(score.relative.score())
# Score: PovScore(Mate(+1), WHITE)
