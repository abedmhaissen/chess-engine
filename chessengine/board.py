from dataclasses import dataclass

FILES = "abcdefgh"
PIECE_VALUES = {"P": 100, "N": 320, "B": 330, "R": 500, "Q": 900, "K": 20000}


def sq(file, rank):
    return rank * 8 + file


def file_of(s):
    return s % 8


def rank_of(s):
    return s // 8


def algebraic(s):
    return f"{FILES[file_of(s)]}{rank_of(s) + 1}"


@dataclass(frozen=True)
class Move:
    frm: int
    to: int
    promo: str = None

    def uci(self):
        s = algebraic(self.frm) + algebraic(self.to)
        if self.promo:
            s += self.promo.lower()
        return s


START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Board:
    def __init__(self, fen=START_FEN):
        self.squares = [None] * 64
        self.white_to_move = True
        self._load_fen(fen)

    def copy(self):
        b = Board.__new__(Board)
        b.squares = list(self.squares)
        b.white_to_move = self.white_to_move
        return b

    def _load_fen(self, fen):
        parts = fen.split()
        placement, side = parts[0], parts[1]
        self.squares = [None] * 64
        rank, file = 7, 0
        for ch in placement:
            if ch == "/":
                rank -= 1
                file = 0
            elif ch.isdigit():
                file += int(ch)
            else:
                self.squares[sq(file, rank)] = ch
                file += 1
        self.white_to_move = side == "w"

    def piece_at(self, s):
        return self.squares[s]

    def is_white(self, piece):
        return piece.isupper()

    def generate_legal_moves(self):
        moves = []
        for m in self._generate_pseudo():
            nb = self.copy()
            nb.make_move(m)
            if not nb._in_check(not nb.white_to_move):
                moves.append(m)
        return moves

    def make_move(self, move):
        piece = self.squares[move.frm]
        self.squares[move.frm] = None
        if move.promo:
            piece = move.promo if self.white_to_move else move.promo.lower()
        elif piece and piece.upper() == "P":
            to_rank = rank_of(move.to)
            if to_rank in (0, 7):
                piece = "Q" if piece.isupper() else "q"
        self.squares[move.to] = piece
        self.white_to_move = not self.white_to_move

    def _in_check(self, for_white):
        king = "K" if for_white else "k"
        try:
            ks = self.squares.index(king)
        except ValueError:
            return True
        saved = self.white_to_move
        self.white_to_move = not for_white
        attacked = any(m.to == ks for m in self._generate_pseudo())
        self.white_to_move = saved
        return attacked

    def _generate_pseudo(self):
        for s, piece in enumerate(self.squares):
            if piece is None:
                continue
            if self.is_white(piece) != self.white_to_move:
                continue
            p = piece.upper()
            if p == "P":
                yield from self._pawn_moves(s, piece)
            elif p == "N":
                yield from self._knight_moves(s)
            elif p == "B":
                yield from self._slide(s, ((1, 1), (1, -1), (-1, 1), (-1, -1)))
            elif p == "R":
                yield from self._slide(s, ((1, 0), (-1, 0), (0, 1), (0, -1)))
            elif p == "Q":
                yield from self._slide(
                    s,
                    ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)),
                )
            elif p == "K":
                yield from self._king_moves(s)

    def _pawn_moves(self, s, piece):
        forward = 1 if piece.isupper() else -1
        start_rank = 1 if piece.isupper() else 6
        f, r = file_of(s), rank_of(s)
        one = sq(f, r + forward)
        if 0 <= r + forward < 8 and self.squares[one] is None:
            yield Move(s, one)
            if r == start_rank:
                two = sq(f, r + 2 * forward)
                if self.squares[two] is None:
                    yield Move(s, two)
        for df in (-1, 1):
            nf, nr = f + df, r + forward
            if 0 <= nf < 8 and 0 <= nr < 8:
                t = sq(nf, nr)
                victim = self.squares[t]
                if victim and self.is_white(victim) != piece.isupper():
                    yield Move(s, t)

    def _knight_moves(self, s):
        f, r = file_of(s), rank_of(s)
        for df, dr in ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)):
            nf, nr = f + df, r + dr
            if 0 <= nf < 8 and 0 <= nr < 8:
                t = sq(nf, nr)
                victim = self.squares[t]
                if victim is None or self.is_white(victim) != self.white_to_move:
                    yield Move(s, t)

    def _king_moves(self, s):
        f, r = file_of(s), rank_of(s)
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                nf, nr = f + df, r + dr
                if 0 <= nf < 8 and 0 <= nr < 8:
                    t = sq(nf, nr)
                    victim = self.squares[t]
                    if victim is None or self.is_white(victim) != self.white_to_move:
                        yield Move(s, t)

    def _slide(self, s, dirs):
        f0, r0 = file_of(s), rank_of(s)
        for df, dr in dirs:
            f, r = f0 + df, r0 + dr
            while 0 <= f < 8 and 0 <= r < 8:
                t = sq(f, r)
                victim = self.squares[t]
                if victim is None:
                    yield Move(s, t)
                else:
                    if self.is_white(victim) != self.white_to_move:
                        yield Move(s, t)
                    break
                f += df
                r += dr
