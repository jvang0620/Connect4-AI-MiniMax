import random
import tkinter as tk
from tkinter import messagebox
import copy

class ConnectFour:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = 'X'
        self.user_wins = 0
        self.computer_wins = 0
        self.ties = 0
        self.create_board()

    def create_board(self):
        self.buttons = []
        for i in range(6):
            row_buttons = []
            for j in range(7):
                button = tk.Button(self.master, text=' ', font=('Arial', 20), width=5, height=2,
                                   command=lambda col=j: self.drop_piece(col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.stats_label = tk.Label(self.master, text="Wins: 0   Losses: 0   Ties: 0", font=('Arial', 12))
        self.stats_label.grid(row=6, columnspan=7)

    def drop_piece(self, col):
        if self.check_valid_move(col):
            row = self.get_next_open_row(col)
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, bg='red' if self.current_player == 'X' else 'blue')
            if self.check_winner(row, col):
                messagebox.showinfo("Connect Four", f"Player {self.current_player} wins!")
                if self.current_player == 'X':
                    self.user_wins += 1
                else:
                    self.computer_wins += 1
                self.update_stats_label()
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Connect Four", "It's a draw!")
                self.ties += 1
                self.update_stats_label()
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O':
                    self.computer_move()

    def check_valid_move(self, col):
        return self.board[0][col] == ' '

    def get_next_open_row(self, col):
        for r in range(5, -1, -1):
            if self.board[r][col] == ' ':
                return r

    def check_winner(self, row, col):
        # Check horizontally
        for c in range(4):
            if self.board[row][c] == self.current_player and \
                    self.board[row][c+1] == self.current_player and \
                    self.board[row][c+2] == self.current_player and \
                    self.board[row][c+3] == self.current_player:
                return True

        # Check vertically
        for r in range(3):
            if self.board[r][col] == self.current_player and \
                    self.board[r+1][col] == self.current_player and \
                    self.board[r+2][col] == self.current_player and \
                    self.board[r+3][col] == self.current_player:
                return True

        # Check positively sloped diagonal
        for r in range(3):
            for c in range(4):
                if self.board[r][c] == self.current_player and \
                        self.board[r+1][c+1] == self.current_player and \
                        self.board[r+2][c+2] == self.current_player and \
                        self.board[r+3][c+3] == self.current_player:
                    return True

        # Check negatively sloped diagonal
        for r in range(3, 6):
            for c in range(4):
                if self.board[r][c] == self.current_player and \
                        self.board[r-1][c+1] == self.current_player and \
                        self.board[r-2][c+2] == self.current_player and \
                        self.board[r-3][c+3] == self.current_player:
                    return True

        return False

    def check_draw(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def reset_board(self):
        for i in range(6):
            for j in range(7):
                self.board[i][j] = ' '
                self.buttons[i][j].config(text=' ', bg='SystemButtonFace')
        self.current_player = 'X'

    def computer_move(self):
        # You can implement the Minimax algorithm here to make the computer's move
        # For simplicity, let's just choose a random valid move
        valid_moves = [col for col in range(7) if self.check_valid_move(col)]
        if valid_moves:
            col = random.choice(valid_moves)
            self.drop_piece(col)

    def update_stats_label(self):
        self.stats_label.config(text=f"Wins: {self.user_wins}   Losses: {self.computer_wins}   Ties: {self.ties}")

def main():
    root = tk.Tk()
    app = ConnectFour(root)
    root.mainloop()

if __name__ == "__main__":
    main()
