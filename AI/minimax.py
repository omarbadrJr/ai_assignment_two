import math
import time
from board import HUMAN, AI
from heuristic import heuristic
from TreeRecorder import TreeRecorder


class Minimax:
    def __init__(self, recorder=None):
        self.h = heuristic()
        self.transposition = {}
        self.start_time = 0
        self.time_limit = None
        self.recorder = recorder if recorder else TreeRecorder()

    def time_up(self):
        return self.time_limit and (time.time() - self.start_time) >= self.time_limit

    def get_move_order(self, board):
        center = board.cols // 2
        return sorted(board.valid_moves(), key=lambda c: abs(c - center))

    def order_moves(self, board, moves, player):
        scored = []
        for c in moves:
            r = board.drop_piece(c, player)
            if r is None:
                val = -math.inf
            else:
                val = self.h.evaluate(board, AI)
                board.undo_top(c)
            scored.append((c, val))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [c for c, _ in scored]

    def tt_lookup(self, board, depth, maximizing):
        return self.transposition.get((board.as_tuple(), depth, maximizing))

    def tt_store(self, board, depth, maximizing, value, move):
        self.transposition[(board.as_tuple(), depth, maximizing)] = (value, move)

    # ✅ Minimax with Alpha-Beta Pruning
    def minimax_with_ab(self, board, depth, maximizing, alpha, beta, level=0, move_col=None):
        if self.time_up():
            return None, None, False

        # Transposition lookup
        tt = self.tt_lookup(board, depth, maximizing)
        if tt:
            value, mv = tt
            self.recorder.node(level, "TT-HIT", move_col, value, alpha, beta)
            return value, mv, True

        # Terminal states
        winner = board.check_winner()
        if winner == AI:
            self.recorder.node(level, "TERMINAL", move_col, math.inf, alpha, beta)
            return math.inf, None, True
        if winner == HUMAN:
            self.recorder.node(level, "TERMINAL", move_col, -math.inf, alpha, beta)
            return -math.inf, None, True
        if depth == 0 or board.is_full():
            val = self.h.evaluate(board, AI)
            self.recorder.node(level, "LEAF", move_col, val, alpha, beta)
            return val, None, True

        # Moves
        valid = board.valid_moves()
        player = AI if maximizing else HUMAN

        # Immediate win check
        for c in valid:
            if board.is_winning_move(c, player):
                v = math.inf if player == AI else -math.inf
                self.recorder.node(level, "IMMEDIATE", c, v, alpha, beta)
                return v, c, True

        # Move ordering
        moves = self.get_move_order(board)
        moves = self.order_moves(board, moves, player)
        best_move = moves[0] if moves else None

        # Enter node
        self.recorder.node(level, "ENTER", move_col, "MAX" if maximizing else "MIN", alpha, beta)

        # MAX player
        if maximizing:
            value = -math.inf
            for c in moves:
                if self.time_up():
                    return None, None, False

                board.drop_piece(c, AI)
                child_val, _, ok = self.minimax_with_ab(board, depth - 1, False, alpha, beta, level + 1, c)
                board.undo_top(c)

                if not ok:
                    return None, None, False

                if child_val is not None and child_val > value:
                    value = child_val
                    best_move = c

                self.recorder.node(level + 1, "child", c, child_val, alpha, beta)

                # Alpha-Beta Pruning
                alpha = max(alpha, value)
                if alpha >= beta:
                    self.recorder.prune(level + 1, alpha, beta)
                    break

            self.tt_store(board, depth, maximizing, value, best_move)
            self.recorder.node(level, "EXIT", move_col, value, alpha, beta)
            return value, best_move, True

        # MIN player
        else:
            value = math.inf
            for c in moves:
                if self.time_up():
                    return None, None, False

                board.drop_piece(c, HUMAN)
                child_val, _, ok = self.minimax_with_ab(board, depth - 1, True, alpha, beta, level + 1, c)
                board.undo_top(c)

                if not ok:
                    return None, None, False

                if child_val is not None and child_val < value:
                    value = child_val
                    best_move = c

                self.recorder.node(level + 1, "child", c, child_val, alpha, beta)

                # Alpha-Beta Pruning
                beta = min(beta, value)
                if beta <= alpha:
                    self.recorder.prune(level + 1, alpha, beta)
                    break

            self.tt_store(board, depth, maximizing, value, best_move)
            self.recorder.node(level, "EXIT", move_col, value, alpha, beta)
            return value, best_move, True

    # ✅ Minimax WITHOUT Pruning
    def minimax_without_pruning(self, board, depth, maximizing, level=0, move_col=None):
        if self.time_up():
            return None, None, False

        # Transposition lookup
        tt = self.tt_lookup(board, depth, maximizing)
        if tt:
            value, mv = tt
            self.recorder.node(level, "TT-HIT", move_col, value, "N/A", "N/A")
            return value, mv, True

        # Terminal states
        winner = board.check_winner()
        if winner == AI:
            self.recorder.node(level, "TERMINAL", move_col, math.inf, "N/A", "N/A")
            return math.inf, None, True
        if winner == HUMAN:
            self.recorder.node(level, "TERMINAL", move_col, -math.inf, "N/A", "N/A")
            return -math.inf, None, True
        if depth == 0 or board.is_full():
            val = self.h.evaluate(board, AI)
            self.recorder.node(level, "LEAF", move_col, val, "N/A", "N/A")
            return val, None, True

        # Moves
        valid = board.valid_moves()
        player = AI if maximizing else HUMAN

        # Immediate win check
        for c in valid:
            if board.is_winning_move(c, player):
                v = math.inf if player == AI else -math.inf
                self.recorder.node(level, "IMMEDIATE", c, v, "N/A", "N/A")
                return v, c, True

        # Move ordering
        moves = self.get_move_order(board)
        moves = self.order_moves(board, moves, player)
        best_move = moves[0] if moves else None

        # Enter node
        self.recorder.node(level, "ENTER", move_col, "MAX" if maximizing else "MIN", "N/A", "N/A")

        # MAX player
        if maximizing:
            value = -math.inf
            for c in moves:
                if self.time_up():
                    return None, None, False

                board.drop_piece(c, AI)
                child_val, _, ok = self.minimax_without_pruning(board, depth - 1, False, level + 1, c)
                board.undo_top(c)

                if not ok:
                    return None, None, False

                if child_val is not None and child_val > value:
                    value = child_val
                    best_move = c

                self.recorder.node(level + 1, "child", c, child_val, "N/A", "N/A")

                # NO PRUNING - examines all nodes

            self.tt_store(board, depth, maximizing, value, best_move)
            self.recorder.node(level, "EXIT", move_col, value, "N/A", "N/A")
            return value, best_move, True

        # MIN player
        else:
            value = math.inf
            for c in moves:
                if self.time_up():
                    return None, None, False

                board.drop_piece(c, HUMAN)
                child_val, _, ok = self.minimax_without_pruning(board, depth - 1, True, level + 1, c)
                board.undo_top(c)

                if not ok:
                    return None, None, False

                if child_val is not None and child_val < value:
                    value = child_val
                    best_move = c

                self.recorder.node(level + 1, "child", c, child_val, "N/A", "N/A")

                # NO PRUNING - examines all nodes

            self.tt_store(board, depth, maximizing, value, best_move)
            self.recorder.node(level, "EXIT", move_col, value, "N/A", "N/A")
            return value, best_move, True

    # Iterative Deepening for both algorithms
    def find_best_move(self, board, max_depth, use_ab=True, time_limit=None):
        self.start_time = time.time()
        self.time_limit = time_limit
        self.recorder.clear()
        best_move = None
        best_value = None

        for depth in range(1, max_depth + 1):
            if self.time_up():
                break
            self.recorder.clear()

            if use_ab:
                val, mv, ok = self.minimax_with_ab(board, depth, True, -math.inf, math.inf)
            else:
                val, mv, ok = self.minimax_without_pruning(board, depth, True)

            if not ok:
                break
            best_value = val
            best_move = mv

        return best_value, best_move

    # ✅ Separate methods for each algorithm
    def find_best_move_with_ab(self, board, max_depth, time_limit=None):
        """Find best move using Minimax WITH Alpha-Beta pruning"""
        self.start_time = time.time()
        self.time_limit = time_limit
        self.recorder.clear()
        best_move = None
        best_value = None

        for depth in range(1, max_depth + 1):
            if self.time_up():
                break
            self.recorder.clear()

            val, mv, ok = self.minimax_with_ab(board, depth, True, -math.inf, math.inf)

            if not ok:
                break
            best_value = val
            best_move = mv

        return best_value, best_move

    def find_best_move_without_pruning(self, board, max_depth, time_limit=None):
        """Find best move using Minimax WITHOUT pruning"""
        self.start_time = time.time()
        self.time_limit = time_limit
        self.recorder.clear()
        best_move = None
        best_value = None

        for depth in range(1, max_depth + 1):
            if self.time_up():
                break
            self.recorder.clear()

            val, mv, ok = self.minimax_without_pruning(board, depth, True)

            if not ok:
                break
            best_value = val
            best_move = mv

        return best_value, best_move