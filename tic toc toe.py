import tkinter as tk
from tkinter import messagebox
import random
import time


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("8x8 Tic Tac Toe")
        self.board_size = 8
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "X"
        self.mode = "User vs User"  # Default mode
        self.difficulty = "Easy"  # Default difficulty level
        self.score = {"X": 0, "O": 0}
        self.move_stack = []  # Stack to keep track of moves
        
        self.time_limit = 360  # Time limit in seconds
        self.start_time = time.time()
        self.timer_running = True
        self.create_widgets()
        self.update_timer()

    def create_widgets(self):
        self.timer_label = tk.Label(self.root, text="Time Left: 60s", font=("Helvetica", 12), fg="green")
        self.timer_label.grid(row=0, column=0, columnspan=4)

        self.mode_label = tk.Label(self.root, text="Mode: User vs User", font=("Helvetica", 12))
        self.mode_label.grid(row=0, column=4, columnspan=4)

        self.score_label = tk.Label(self.root, text=f"Score - X: {self.score['X']} | O: {self.score['O']}", font=("Helvetica", 12))
        self.score_label.grid(row=0, column=8, columnspan=4)

        self.reset_button = tk.Button(self.root, text="Restart Game", command=self.reset_board, bg="orange", fg="white")
        self.reset_button.grid(row=9, column=0, columnspan=2)

        self.switch_mode_button = tk.Button(self.root, text="Switch to User vs AI", command=self.switch_mode, bg="cyan", fg="black")
        self.switch_mode_button.grid(row=9, column=2, columnspan=2)

        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo_move, bg="yellow", fg="black")
        self.undo_button.grid(row=9, column=4, columnspan=2)

        self.exit_button = tk.Button(self.root, text="Exit Game", command=self.root.quit, bg="red", fg="white")
        self.exit_button.grid(row=9, column=6, columnspan=2)

        self.difficulty_menu = tk.Menubutton(self.root, text="Difficulty: Easy", relief=tk.RAISED, bg="lightgreen")
        self.difficulty_menu.menu = tk.Menu(self.difficulty_menu, tearoff=0)
        self.difficulty_menu["menu"] = self.difficulty_menu.menu
        for level in ["Easy", "Medium", "Hard"]:
            self.difficulty_menu.menu.add_command(label=level, command=lambda l=level: self.set_difficulty(l))
        self.difficulty_menu.grid(row=9, column=8, columnspan=2)

        for row in range(self.board_size):
            for col in range(self.board_size):
                button = tk.Button(
                    self.root,
                    text="",
                    font=("Helvetica", 20),
                    width=3,
                    height=1,
                    bg="lightgrey",
                    command=lambda r=row, c=col: self.on_click(r, c),
                )
                button.grid(row=row + 1, column=col)
                self.board[row][col] = button

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            remaining_time = self.time_limit - elapsed_time

            if remaining_time > 0:
                self.timer_label.config(text=f"Time Left: {remaining_time}s")
                self.root.after(1000, self.update_timer)
            else:
                self.timer_label.config(text="Time Left: 0s", fg="red")
                self.timer_running = False
                messagebox.showinfo("Game Over", "Time's up! The game is a draw.")
                self.reset_board()

    def set_difficulty(self, level):
        self.difficulty = level
        self.difficulty_menu.config(text=f"Difficulty: {level}")

    def switch_mode(self):
        if self.mode == "User vs User":
            self.mode = "User vs AI"
            self.mode_label.config(text="Mode: User vs AI")
            self.switch_mode_button.config(text="Switch to User vs User")
        else:
            self.mode = "User vs User"
            self.mode_label.config(text="Mode: User vs User")
            self.switch_mode_button.config(text="Switch to User vs AI")
        self.reset_board()

    def on_click(self, row, col):
        button = self.board[row][col]
        if button["text"] == "" and self.timer_running:
            button["text"] = self.current_player
            button["fg"] = "blue" if self.current_player == "X" else "red"
            self.move_stack.append((row, col))  # Record the move
            if self.check_winner(row, col):
                self.score[self.current_player] += 1
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.update_score()
                self.reset_board()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.mode == "User vs AI" and self.current_player == "O":
                    self.ai_move()

    def undo_move(self):
        if self.move_stack and self.timer_running:
            last_move = self.move_stack.pop()
            row, col = last_move
            self.board[row][col]["text"] = ""  # Clear the last move
            self.board[row][col]["bg"] = "lightgrey"
            self.current_player = "O" if self.current_player == "X" else "X"  # Switch back to the previous player
        else:
            messagebox.showinfo("Undo", "No moves to undo!")

    def ai_move(self):
        empty_cells = [(r, c) for r in range(self.board_size) for c in range(self.board_size) if self.board[r][c]["text"] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.on_click(row, col)

    def check_winner(self, row, col):
        directions = [
            [(0, 1), (0, -1)],
            [(1, 0), (-1, 0)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)],
        ]

        for direction in directions:
            count = 1
            for dx, dy in direction:
                count += self.count_in_direction(row, col, dx, dy)

            if count >= 5:
                return True

        return False

    def count_in_direction(self, row, col, dx, dy):
        count = 0
        player = self.current_player

        for _ in range(4):
            row += dx
            col += dy

            if 0 <= row < self.board_size and 0 <= col < self.board_size:
                if self.board[row][col]["text"] == player:
                    count += 1
                else:
                    break
            else:
                break

        return count

    def is_draw(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col]["text"] == "":
                    return False
        return True

    def update_score(self):
        self.score_label.config(text=f"Score - X: {self.score['X']} | O: {self.score['O']}")

    def reset_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.board[row][col]["text"] = ""
                self.board[row][col]["bg"] = "lightgrey"
        self.move_stack.clear()  # Clear the move stack
        self.current_player = "X"
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
