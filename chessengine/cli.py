import sys

from chessengine.board import Board, algebraic
from chessengine.engine import evaluate, search_best_move


def render(board):
    rows = []
    for rank in range(7, -1, -1):
        cells = []
        for file in range(8):
            p = board.squares[rank * 8 + file]
            cells.append(p if p else ".")
        rows.append(f"{rank + 1} " + " ".join(cells))
    rows.append("  a b c d e f g h")
    side = "White" if board.white_to_move else "Black"
    rows.append(f"{side} to move | eval={evaluate(board)}")
    return "\n".join(rows)


def main():
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    if depth < 1:
        raise SystemExit("depth must be >= 1")
    board = Board()
    print(f"chess-engine · depth={depth} · type q to quit")
    print(render(board))
    while True:
        moves = board.generate_legal_moves()
        if not moves:
            print("Game over.")
            break
        if board.white_to_move:
            raw = input("Your move (uci, e.g. e2e4): ").strip().lower()
            if raw in {"q", "quit", "exit"}:
                break
            chosen = next((m for m in moves if m.uci() == raw), None)
            if chosen is None:
                print("Illegal move. Try again (example: e2e4).")
                continue
            board.make_move(chosen)
        else:
            move, score = search_best_move(board, depth=depth)
            if move is None:
                print("Engine resigns / no move.")
                break
            print(f"Engine plays {move.uci()} (score={score})")
            board.make_move(move)
        print(render(board))


if __name__ == "__main__":
    main()
