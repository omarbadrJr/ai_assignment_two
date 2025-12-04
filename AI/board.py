EMPTY = 0
HUMAN = 1
AI = 2

class Board:
    def __init__(self, rows=6, cols=7, grid=None):
        self.rows = rows
        self.cols = cols
        if grid:
            self.grid = [list(r) for r in grid]
        else:
            self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]

    def clone(self):
        return Board(self.rows, self.cols, [row[:] for row in self.grid])

    def as_tuple(self):
        return tuple(tuple(row) for row in self.grid)

    def valid_moves(self):
        return [c for c in range(self.cols) if self.grid[0][c] == EMPTY]

    def is_full(self):
        return all(self.grid[0][c] != EMPTY for c in range(self.cols))

    def drop_piece(self, col, player):
        if col < 0 or col >= self.cols:
            return None
        if self.grid[0][col] != EMPTY:
            return None
        for r in range(self.rows - 1, -1, -1):
            if self.grid[r][col] == EMPTY:
                self.grid[r][col] = player
                return r
        return None

    def undo_top(self, col):
        for r in range(self.rows):
            if self.grid[r][col] != EMPTY:
                self.grid[r][col] = EMPTY
                return True
        return False

    def check_winner(self):
        g = self.grid
        R, C = self.rows, self.cols

        # Horizontal
        for r in range(R):
            for c in range(C - 3):
                v = g[r][c]
                if v != EMPTY and v == g[r][c+1] == g[r][c+2] == g[r][c+3]:
                    return v

        # Vertical
        for c in range(C):
            for r in range(R - 3):
                v = g[r][c]
                if v != EMPTY and v == g[r+1][c] == g[r+2][c] == g[r+3][c]:
                    return v

        # Diagonal down-right
        for r in range(R - 3):
            for c in range(C - 3):
                v = g[r][c]
                if v != EMPTY and v == g[r+1][c+1] == g[r+2][c+2] == g[r+3][c+3]:
                    return v

        # Diagonal up-right
        for r in range(3, R):
            for c in range(C - 3):
                v = g[r][c]
                if v != EMPTY and v == g[r-1][c+1] == g[r-2][c+2] == g[r-3][c+3]:
                    return v

        return None

    def is_winning_move(self, col, player):
        row = self.drop_piece(col, player)
        if row is None:
            return False
        winner = self.check_winner()
        self.undo_top(col)
        return winner == player

    def print(self):
        print("\nBoard:")
        symbols = {EMPTY: ".", HUMAN: "X", AI: "O"}
        for r in range(self.rows):
            print(" ".join(symbols[self.grid[r][c]] for c in range(self.cols)))
        print(" ".join(str(i) for i in range(self.cols)))
