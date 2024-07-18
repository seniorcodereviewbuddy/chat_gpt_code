class Square:
    def __init__(self, algebraic: str):
        self.algebraic = algebraic
        self.row = int(algebraic[1]) - 1
        self.col = ord(algebraic[0]) - ord("a")

    # @classmethod
    # def square_from_row_col(cls, row: int, col: int) -> "Square":

    def __str__(self) -> str:
        return self.algebraic

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Square):
            return NotImplemented
        return self.algebraic == other.algebraic

    def __hash__(self) -> int:
        return hash(self.algebraic)


class Squares:
    A1 = Square("a1")
    A2 = Square("a2")
    A3 = Square("a3")
    A4 = Square("a4")
    A5 = Square("a5")
    A6 = Square("a6")
    A7 = Square("a7")
    A8 = Square("a8")
    B1 = Square("b1")
    B2 = Square("b2")
    B3 = Square("b3")
    B4 = Square("b4")
    B5 = Square("b5")
    B6 = Square("b6")
    B7 = Square("b7")
    B8 = Square("b8")
    C1 = Square("c1")
    C2 = Square("c2")
    C3 = Square("c3")
    C4 = Square("c4")
    C5 = Square("c5")
    C6 = Square("c6")
    C7 = Square("c7")
    C8 = Square("c8")
    D1 = Square("d1")
    D2 = Square("d2")
    D3 = Square("d3")
    D4 = Square("d4")
    D5 = Square("d5")
    D6 = Square("d6")
    D7 = Square("d7")
    D8 = Square("d8")
    E1 = Square("e1")
    E2 = Square("e2")
    E3 = Square("e3")
    E4 = Square("e4")
    E5 = Square("e5")
    E6 = Square("e6")
    E7 = Square("e7")
    E8 = Square("e8")
    F1 = Square("f1")
    F2 = Square("f2")
    F3 = Square("f3")
    F4 = Square("f4")
    F5 = Square("f5")
    F6 = Square("f6")
    F7 = Square("f7")
    F8 = Square("f8")
    G1 = Square("g1")
    G2 = Square("g2")
    G3 = Square("g3")
    G4 = Square("g4")
    G5 = Square("g5")
    G6 = Square("g6")
    G7 = Square("g7")
    G8 = Square("g8")
    H1 = Square("h1")
    H2 = Square("h2")
    H3 = Square("h3")
    H4 = Square("h4")
    H5 = Square("h5")
    H6 = Square("h6")
    H7 = Square("h7")
    H8 = Square("h8")

    square_in_order = (
        A1,
        A2,
        A3,
        A4,
        A5,
        A6,
        A7,
        A8,
        B1,
        B2,
        B3,
        B4,
        B5,
        B6,
        B7,
        B8,
        C1,
        C2,
        C3,
        C4,
        C5,
        C6,
        C7,
        C8,
        D1,
        D2,
        D3,
        D4,
        D5,
        D6,
        D7,
        D8,
        E1,
        E2,
        E3,
        E4,
        E5,
        E6,
        E7,
        E8,
        F1,
        F2,
        F3,
        F4,
        F5,
        F6,
        F7,
        F8,
        G1,
        G2,
        G3,
        G4,
        G5,
        G6,
        G7,
        G8,
        H1,
        H2,
        H3,
        H4,
        H5,
        H6,
        H7,
        H8,
    )

    @classmethod
    def square_from_row_col(cls, row: int, col: int) -> Square:
        index = col * 8 + row
        return cls.square_in_order[index]
