import tkinter as tk
from tkinter import messagebox, scrolledtext
from board import Board, HUMAN, AI
from minimax import Minimax

class SimpleConnect4:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect 4")
        self.master.geometry("1200x700") # Increased size for side-by-side layout
        
        # Initialize Game Logic
        self.board = Board(rows=6, cols=7)
        self.minimax = Minimax()
        self.use_pruning = True
        self.ai_move_count = 0 # Track AI moves
        
        # Main layout container
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- SCREEN 1: SELECTION ---
        self.selection_frame = tk.Frame(self.main_frame)
        self.selection_frame.pack()

        self.lbl = tk.Label(self.selection_frame, text="Choose AI Algorithm:", font=("Arial", 14))
        self.lbl.pack(pady=20)

        self.btn1 = tk.Button(self.selection_frame, text="With Alpha-Beta Pruning", command=lambda: self.setup_board(True))
        self.btn1.pack(pady=5)

        self.btn2 = tk.Button(self.selection_frame, text="Without Pruning", command=lambda: self.setup_board(False))
        self.btn2.pack(pady=5)

        # Game Area (Board + Log)
        self.game_frame = tk.Frame(self.main_frame)
        
        # Canvas for the game (Left side)
        self.canvas = tk.Canvas(self.game_frame, width=700, height=600, bg="blue")
        
        # Tree Log (Right side)
        self.log_frame = tk.Frame(self.game_frame)
        self.log_label = tk.Label(self.log_frame, text="Minimax Tree Log", font=("Arial", 12, "bold"))
        self.log_label.pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(self.log_frame, width=60, height=35, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.configure(state='disabled')

    def setup_board(self, pruning):
        """Removes buttons and shows the game board."""
        self.use_pruning = pruning
        
        # Clear the selection screen
        self.selection_frame.pack_forget()

        # Show the game area
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas.pack(side=tk.LEFT, padx=10)
        self.log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
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
                self.ai_move_count += 1 # Increment AI move count
                self.show_tree_log() # Show the tree log after AI move
                if self.check_game_over(AI): return

    def show_tree_log(self):
        """Displays the Minimax search tree in the side panel."""
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END) # Clear previous log

        header = f"========================================\nAI Move #{self.ai_move_count}\n========================================\n"
        self.log_text.insert(tk.END, header)

        for level, line in self.minimax.recorder.lines:
            indent = "  " * level
            self.log_text.insert(tk.END, f"{indent}{line}\n")
        
        self.log_text.configure(state='disabled') # Make read-only
        self.log_text.see(tk.END) # Scroll to bottom

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