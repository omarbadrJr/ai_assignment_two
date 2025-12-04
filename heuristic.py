from board import EMPTY, HUMAN, AI

class heuristic:
    def __init__(self):
        # Weights tuned for medium strength play
        self.W4 = 10000     # four-in-a-row
        self.W3 = 100       # open three
        self.W2 = 10        # open two
        self.opp_W3 = -120  # opponent open three (threat)
        self.center_weight = 3

    def evaluate_window(self, window, player):

        opp = HUMAN if player == AI else AI
        count_p = window.count(player)
        count_o = window.count(opp)
        count_empty = window.count(EMPTY)

        score = 0

        # favorable windows for player
        if count_o == 0:
            if count_p == 4:
                score += self.W4
            elif count_p == 3 and count_empty == 1:
                score += self.W3
            elif count_p == 2 and count_empty == 2:
                score += self.W2

        # opponent threat
        if count_p == 0 and count_o == 3 and count_empty == 1:
            score += self.opp_W3

        return score

    def evaluate(self, board, player):

        g = board.grid
        R, C = board.rows, board.cols
        score = 0

        # center column control
        center = C // 2
        score += sum(1 for r in range(R) if g[r][center] == player) * self.center_weight

        # horizontal windows
        for r in range(R):
            for c in range(C - 3):
                window = [g[r][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        # vertical windows
        for c in range(C):
            for r in range(R - 3):
                window = [g[r+i][c] for i in range(4)]
                score += self.evaluate_window(window, player)

        # diagonal down-right
        for r in range(R - 3):
            for c in range(C - 3):
                window = [g[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        # diagonal up-right
        for r in range(3, R):
            for c in range(C - 3):
                window = [g[r-i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score