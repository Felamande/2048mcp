import tkinter as tk
from tkinter import messagebox
from game_logic import GameLogic
import threading # To run the game logic updates separately

class GameGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('2048 Game')
        self.game = GameLogic()
        self.grid_cells = []
        self.init_grid()
        self.update_grid()
        self.master.bind("<Key>", self.key_press)
        # Prevent resizing
        self.master.resizable(False, False)

    def init_grid(self):
        background = tk.Frame(self, bg='#92877d', bd=3, width=400, height=400)
        background.grid(pady=(80, 0)) # Add padding on top for score

        for i in range(self.game.size):
            grid_row = []
            for j in range(self.game.size):
                cell = tk.Frame(background, bg='#eee4da', width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                t = tk.Label(master=cell, text="", bg='#eee4da', justify=tk.CENTER, font=('Helvetica', 30, 'bold'), width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

        # Score display
        self.score_label = tk.Label(self, text=f"Score: {self.game.score}", font=('Helvetica', 18, 'bold'))
        self.score_label.place(relx=0.5, y=40, anchor='center') # Place score above the grid

    def update_grid(self):
        """Updates the GUI grid based on the game board state."""
        for i in range(self.game.size):
            for j in range(self.game.size):
                value = self.game.board[i][j]
                cell_label = self.grid_cells[i][j]
                if value == 0:
                    cell_label.configure(text="", bg='#cdc1b4')
                else:
                    text_color, bg_color = self.get_tile_colors(value)
                    cell_label.configure(text=str(value), bg=bg_color, fg=text_color)
        self.score_label.configure(text=f"Score: {self.game.score}")
        self.update_idletasks() # Force GUI update

    def get_tile_colors(self, value):
        """Returns text and background colors for a given tile value."""
        colors = {
            0: ('#776e65', '#cdc1b4'),
            2: ('#776e65', '#eee4da'),
            4: ('#776e65', '#ede0c8'),
            8: ('#f9f6f2', '#f2b179'),
            16: ('#f9f6f2', '#f59563'),
            32: ('#f9f6f2', '#f67c5f'),
            64: ('#f9f6f2', '#f65e3b'),
            128: ('#f9f6f2', '#edcf72'),
            256: ('#f9f6f2', '#edcc61'),
            512: ('#f9f6f2', '#edc850'),
            1024: ('#f9f6f2', '#edc53f'),
            2048: ('#f9f6f2', '#edc22e'),
            # Add colors for higher tiles
            4096: ('#f9f6f2', '#60d9f0'), # Light Blue
            8192: ('#f9f6f2', '#8a5ff0'), # Purple
            16384: ('#f9f6f2', '#5ff08a'), # Green
            32768: ('#f9f6f2', '#f05f5f'), # Red
        }
        # Default for higher values
        default_color = ('#f9f6f2', '#3c3a32')
        return colors.get(value, default_color)

    def key_press(self, event):
        """Handles keyboard input."""
        if self.game.game_over:
            return # Ignore input if game is over

        key = event.keysym
        moved = False
        if key == 'Up':
            moved = self.game.move('up')
        elif key == 'Down':
            moved = self.game.move('down')
        elif key == 'Left':
            moved = self.game.move('left')
        elif key == 'Right':
            moved = self.game.move('right')

        if moved:
            self.update_grid()
            if self.game.game_over:
                self.show_game_over()

    def show_game_over(self):
        """Displays the game over message."""
        messagebox.showinfo("Game Over", f"Game Over! Your score: {self.game.score}")

    def update_game_state(self, new_state):
        """Updates the GUI based on a new game state dictionary (from API)."""
        self.game.board = new_state['board']
        self.game.score = new_state['score']
        self.game.game_over = new_state['game_over']
        self.update_grid()
        if self.game.game_over:
            # Check if game over message already shown to avoid duplicates
            # This simple check might not be robust enough in complex scenarios
            # A more robust way would be to track the state explicitly.
            # For now, let's assume the API call causing game over will trigger this once.
            self.show_game_over()


def run_gui():
    """Initializes and runs the Tkinter GUI."""
    root = tk.Tk()
    gui = GameGUI(master=root)
    gui.pack()
    root.mainloop()

if __name__ == "__main__":
    # Run the GUI in the main thread
    run_gui()