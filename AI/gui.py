import tkinter as tk
from tkinter import messagebox
from board import Board, HUMAN, AI
from minimax import Minimax

class SimpleConnect4:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect 4")
        
        # Initialize Game Logic
        self.board = Board(rows=6, cols=7)
        self.minimax = Minimax()
        self.use_pruning = True
        
        # --- SCREEN 1: SELECTION ---
        self.lbl = tk.Label(master, text="Choose AI Algorithm:", font=("Arial", 14))
        self.lbl.pack(pady=20)

        self.btn1 = tk.Button(master, text="With Alpha-Beta Pruning", command=lambda: self.setup_board(True))
        self.btn1.pack(pady=5)

        self.btn2 = tk.Button(master, text="Without Pruning", command=lambda: self.setup_board(False))
        self.btn2.pack(pady=5)

        # Canvas for the game (hidden initially)
        self.canvas = tk.Canvas(master, width=700, height=600, bg="blue")

    def setup_board(self, pruning):
        """Removes buttons and shows the game board."""
        self.use_pruning = pruning
        
        # Clear the selection screen
        self.lbl.destroy()
        self.btn1.destroy()
        self.btn2.destroy()

        # Show the board
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()

    def draw_board(self):
        """Draws the grid based on board state."""
        self.canvas.delete("all")
        for r in range(6):
            for c in range(7):
                x, y = c * 100, r * 100
                piece = self.board.grid[r][c]
                color = "white"
                if piece == HUMAN: color = "red"
                elif piece == AI: color = "yellow"
                
                self.canvas.create_oval(x + 10, y + 10, x + 90, y + 90, fill=color, outline="black")
    
    def handle_click(self, event):
        """Main Game Loop: Human Move -> Check Win -> AI Move -> Check Win"""
        col = event.x // 100  # Calculate column from mouse X position

        # 1. HUMAN TURN
        if col in self.board.valid_moves():
            self.board.drop_piece(col, HUMAN)
            self.draw_board()
            self.master.update()  # Force screen update so we see the red piece immediately

            if self.check_game_over(HUMAN): return

            # 2. AI TURN
            # Select algorithm based on previous choice
            depth = 4
            if self.use_pruning:
                _, move = self.minimax.find_best_move_with_ab(self.board, depth)
            else:
                _, move = self.minimax.find_best_move_without_pruning(self.board, depth)

            if move is not None:
                self.board.drop_piece(move, AI)
                self.draw_board()
                if self.check_game_over(AI): return

    def check_game_over(self, player):
        winner = self.board.check_winner()
        if winner == player:
            text = "You Win!" if player == HUMAN else "AI Wins!"
            messagebox.showinfo("Game Over", text)
            self.master.destroy() # Close window
            return True
        elif self.board.is_full():
            messagebox.showinfo("Game Over", "Draw!")
            self.master.destroy()
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = SimpleConnect4(root)
    root.mainloop()