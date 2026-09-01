chess-engine

tiny python chess engine. minimax + alpha beta material + piece square tables. u play it in the terminal.

no castling or en passant yet. its v0 on purpose.

PYTHONPATH=. python -m unittest discover -s tests -v
PYTHONPATH=. python -m chessengine.cli 3

moves are uci style like e2e4. you play white.

i play chess a lot. chess.com: abedcool add me if u want

next i wanna do castling / en passant a transposition table and iterative deepening
