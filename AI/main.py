import time
from board import Board, HUMAN, AI
from minimax import Minimax
from tree import TreeTXT
from TreeRecorder import TreeRecorder


def print_board(board):

    print("\n" + "=" * 50)
    print("   CONNECT 4 GAME")
    print("=" * 50)
    board.print()
    print()


def human_turn(board):
    while True:
        try:
            col = int(input(f"Enter column (0-{board.cols - 1}): "))
            if col in board.valid_moves():
                return col
            else:
                print(" Invalid move! Try again.")
        except ValueError:
            print(" Please enter a valid integer!")


def ai_turn(board, minimax, depth, use_ab=True, time_limit=None, save_tree=False):
    print(" AI is thinking...")

    # Clear previous tree recordings
    minimax.recorder.clear()

    if use_ab:
        value, move = minimax.find_best_move_with_ab(board, depth, time_limit)
        algorithm = "with Alpha-Beta"
    else:
        value, move = minimax.find_best_move_without_pruning(board, depth, time_limit)
        algorithm = "without pruning"

    print(f" AI chose column {move} (value: {value}) - {algorithm}")

    # Save tree if requested
    if save_tree and minimax.recorder.lines:
        tree_saver = TreeTXT()
        filename = f"ai_move_{int(time.time())}.txt"
        tree_saver.save(minimax.recorder.lines, filename)
        print(f" AI decision tree saved to: {filename}")

    return move, minimax.recorder.lines


def save_game_tree(tree_lines, filename_prefix):
    """Save the game tree to a file"""
    if tree_lines:
        tree_saver = TreeTXT()
        filename = f"{filename_prefix}_{int(time.time())}.txt"
        tree_saver.save(tree_lines, filename)
        print(f" Game tree saved to: {filename}")
        return filename
    return None


def play_game_with_tree_recording():
    # Game settings
    ROWS, COLS = 6, 7
    AI_DEPTH = 4
    USE_ALPHA_BETA = True
    TIME_LIMIT = 10  # seconds

    # Create objects with tree recorder
    board = Board(ROWS, COLS)
    recorder = TreeRecorder()
    minimax = Minimax(recorder)

    # Store all game trees
    game_trees = []

    print(" Welcome to Connect 4 with Tree Recording!")
    print("  = empty cell")
    print(" X = You (Human)")
    print(" O = AI")
    print(" All AI moves will have decision trees saved!")

    # Choose who starts first
    first_player = input("\nWho starts first? (1 for Human, 2 for AI, Enter for random): ")
    if first_player == "1":
        current_player = HUMAN
    elif first_player == "2":
        current_player = AI
    else:
        import random
        current_player = random.choice([HUMAN, AI])
        print(f" Player {current_player} starts first (random)")

    # Main game loop
    move_count = 0
    while True:
        print_board(board)
        move_count += 1

        # Check game state
        winner = board.check_winner()
        if winner:
            if winner == HUMAN:
                print(" You won! Congratulations!")
            else:
                print(" AI won!")
            break

        if board.is_full():
            print("⚖ It's a tie!")
            break

        # Current player's turn
        if current_player == HUMAN:
            col = human_turn(board)
            board.drop_piece(col, HUMAN)
            print(f" You played in column {col}")
        else:
            col, tree_lines = ai_turn(board, minimax, AI_DEPTH, USE_ALPHA_BETA, TIME_LIMIT, save_tree=True)
            if col is not None:
                board.drop_piece(col, AI)
                # Store the tree for this AI move
                if tree_lines:
                    game_trees.append({
                        'move_number': move_count,
                        'column': col,
                        'tree_lines': tree_lines.copy()
                    })
            else:
                print(" AI timed out, playing random move")
                valid_moves = board.valid_moves()
                if valid_moves:
                    import random
                    col = random.choice(valid_moves)
                    board.drop_piece(col, AI)

        # Switch players
        current_player = AI if current_player == HUMAN else HUMAN

    # End of game
    print_board(board)

    # Save all game trees
    if game_trees and input("\nSave all game trees? (y/n): ").lower() == 'y':
        for i, game_tree in enumerate(game_trees):
            filename = f"full_game_move_{game_tree['move_number']}_col_{game_tree['column']}.txt"
            tree_saver = TreeTXT()
            tree_saver.save(game_tree['tree_lines'], filename)
            print(f"Saved tree for move {game_tree['move_number']} to: {filename}")




def compare_algorithms_with_trees():
    print("\n🔬 Algorithm Comparison with Tree Recording")
    print("=" * 50)

    # Test position
    test_board = Board(6, 7)
    test_board.drop_piece(3, HUMAN)
    test_board.drop_piece(3, AI)
    test_board.drop_piece(4, HUMAN)

    print("Test board position:")
    test_board.print()

    depth = 3
    time_limit = 5

    # Test with Alpha-Beta
    print("\n1. With Alpha-Beta Pruning:")
    recorder_ab = TreeRecorder()
    minimax_ab = Minimax(recorder_ab)

    start_time = time.time()
    value_ab, move_ab = minimax_ab.find_best_move_with_ab(test_board, depth, time_limit)
    time_ab = time.time() - start_time

    print(f"   Result: {value_ab}, Move: {move_ab}")
    print(f"   Time: {time_ab:.3f} seconds")
    print(f"   Nodes in tree: {len(recorder_ab.lines)}")

    # Save alpha-beta tree
    if recorder_ab.lines:
        tree_saver = TreeTXT()
        filename_ab = f"alphabeta_tree_{int(time.time())}.txt"
        tree_saver.save(recorder_ab.lines, filename_ab)
        print(f"    Alpha-Beta tree saved to: {filename_ab}")

    # Test without Alpha-Beta
    print("\n2. Without Alpha-Beta Pruning:")
    recorder_noab = TreeRecorder()
    minimax_noab = Minimax(recorder_noab)

    start_time = time.time()
    value_noab, move_noab = minimax_noab.find_best_move_without_pruning(test_board, depth, time_limit)
    time_noab = time.time() - start_time

    print(f"   Result: {value_noab}, Move: {move_noab}")
    print(f"   Time: {time_noab:.3f} seconds")
    print(f"   Nodes in tree: {len(recorder_noab.lines)}")

    # Save no-pruning tree
    if recorder_noab.lines:
        tree_saver = TreeTXT()
        filename_noab = f"nopruning_tree_{int(time.time())}.txt"
        tree_saver.save(recorder_noab.lines, filename_noab)
        print(f"   No-Pruning tree saved to: {filename_noab}")

    # Comparison results
    print("\n Comparison Results:")
    if time_ab > 0:
        speed_improvement = time_noab / time_ab
        print(f"   Speed improvement: {speed_improvement:.2f}x faster with Alpha-Beta")

    if recorder_noab.lines and recorder_ab.lines:
        node_reduction = (1 - len(recorder_ab.lines) / len(recorder_noab.lines)) * 100
        print(f"   Node reduction: {node_reduction:.2f}% with Alpha-Beta")


def show_tree_recording_info():
    print("\n" + "=" * 50)
    print("        TREE RECORDING INFORMATION")
    print("=" * 50)
    print(" Tree Recording captures the complete decision process:")
    print("\n What gets recorded:")
    print("   • ENTER nodes - When algorithm enters a new state")
    print("   • LEAF nodes - Terminal or depth-limited positions")
    print("   • TERMINAL nodes - Win/loss/draw states")
    print("   • IMMEDIATE nodes - Winning moves found")
    print("   • TT-HIT nodes - Transposition table cache hits")
    print("   • PRUNED branches - Alpha-Beta cutoffs")
    print("   • EXIT nodes - Returning from recursive calls")
    print("\n Information captured:")
    print("   • Node type and level")
    print("   • Move column")
    print("   • Value (score)")
    print("   • Alpha-Beta bounds")
    print("\n Files are saved as text with tree visualization")


def main():
    while True:
        print("\n" + "=" * 50)
        print("        CONNECT 4 - TREE RECORDING DEMO")
        print("=" * 50)
        print("1.  Play Game with Tree Recording")
        print("2.  Compare Algorithms with Trees")
        print("3.  Show Tree Recording Info")
        print("4.  Exit")

        choice = input("\nChoose an option (1-5): ")

        if choice == "1":
            play_game_with_tree_recording()
        elif choice == "2":
            compare_algorithms_with_trees()
        elif choice == "3":
            show_tree_recording_info()
        elif choice == "4":
            print(" Goodbye!")
            break
        else:
            print(" Invalid choice!")


if __name__ == "__main__":
    main()