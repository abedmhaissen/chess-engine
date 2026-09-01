from chessengine.board import PIECE_VALUES, Board, Move, file_of, rank_of

PST = {
    "P": [
        0, 0, 0, 0, 0, 0, 0, 0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5, 5, 10, 25, 25, 10, 5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, -5, -10, 0, 0, -10, -5, 5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0,
    ],
    "N": [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50,
    ],
    "B": [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20,
    ],
    "R": [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        0, 0, 0, 5, 5, 0, 0, 0,
    ],
    "Q": [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20,
    ],
    "K": [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20, 0, 0, 0, 0, 20, 20,
        20, 30, 10, 0, 0, 10, 30, 20,
    ],
}


def evaluate(board):
    score = 0
    for s, piece in enumerate(board.squares):
        if piece is None:
            continue
        kind = piece.upper()
        val = PIECE_VALUES[kind]
        table = PST.get(kind, [0] * 64)
        idx = s if piece.isupper() else (63 - s)
        pst = table[idx]
        contrib = val + pst
        score += contrib if piece.isupper() else -contrib
    return score


def order_moves(board, moves):
    def key(m):
        victim = board.piece_at(m.to)
        return PIECE_VALUES.get(victim.upper(), 0) if victim else 0

    return sorted(moves, key=key, reverse=True)


def alphabeta(board, depth, alpha, beta):
    if depth == 0:
        return evaluate(board), None

    moves = order_moves(board, board.generate_legal_moves())
    if not moves:
        in_check = board._in_check(board.white_to_move)
        if in_check:
            return (-100000 + (10 - depth) if board.white_to_move else 100000 - (10 - depth)), None
        return 0, None

    best_move = None
    if board.white_to_move:
        value = -10**9
        for m in moves:
            nb = board.copy()
            nb.make_move(m)
            score, _ = alphabeta(nb, depth - 1, alpha, beta)
            if score > value:
                value, best_move = score, m
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move
    else:
        value = 10**9
        for m in moves:
            nb = board.copy()
            nb.make_move(m)
            score, _ = alphabeta(nb, depth - 1, alpha, beta)
            if score < value:
                value, best_move = score, m
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_move


def search_best_move(board, depth=3):
    score, move = alphabeta(board, depth, -10**9, 10**9)
    return move, score
