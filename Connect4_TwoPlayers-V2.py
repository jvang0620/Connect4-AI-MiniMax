# for representing the board as a matrix and doing operations on it
import numpy as np
# for gui
import pygame
# for exiting the gui
import sys
# for calulations, for exampel with infinity
import math
# for delaying execution of certain events
from threading import Timer
# for generating random values, for example for 1st turn
import random


# global constant variables
# -------------------------------

# row and column count
ROWS = 6
COLS = 7

# pieces represented as numbers
PLAYER_ONE = 1
PLAYER_TWO = 2

# colors for GUI
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# various functions used by the game
# -------------------------------

# using numpy, create an empty matrix of 6 rows and 7 columns
def create_board():
    board = np.zeros((ROWS, COLS))
    return board


# add a piece to a given location, i.e., set a position in the matrix as 1 or 2
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# checking that the top row of the selected column is still not filled
# i.e., that there is still space in the current column
# note that indexing starts at 0
def is_valid_location(board, col):
    return board[0][col] == 0


# checking where the piece will fall in the current column
# i.e., finding the first zero row in the given column
def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r


# calculating if the current state of the board for player or AI is a win
def winning_move(board, piece):
    # checking horizontal 'windows' of 4 for win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # checking vertical 'windows' of 4 for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # checking positively sloped diagonals for win
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    # checking negatively sloped diagonals for win
    for c in range(3,COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                return True


# visually representing the board using pygame
# for each position in the matrix the board is either filled with an empty black circle, or a player red/yellow circle
def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE ))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else :
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)

    pygame.display.update()


# checking if the given turn or in other words node in the minimax tree is terminal
# a terminal node is player winning, AI winning or board being filled up
def is_terminal_node(board):
    return winning_move(board, PLAYER_ONE) or winning_move(board, PLAYER_TWO) or len(get_valid_locations(board)) == 0


# get all columns where a piece can be
def get_valid_locations(board):
    valid_locations = []
    
    for column in range(COLS):
        if is_valid_location(board, column):
            valid_locations.append(column)

    return valid_locations


# end the game which will close the window eventually
def end_game():
    global game_over
    game_over = True
    print(game_over)


# various state tracker variables taht use the above fucntions
# -------------------------------

# initializing the board
board = create_board()

# initially nobody has won yet
game_over = False

# initially the game is not over - this is used for GUI quirks
not_over = True

# initial turn is random
turn = PLAYER_ONE

# initializing pygame
pygame.init()

# size of one game location
SQUARESIZE = 100

# dimensions for pygame GUI
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)

# font for win message
my_font = pygame.font.SysFont("monospace", 75)

# draw GUI
draw_board(board)
pygame.display.update()


# game loop
# -------------------------------

# loop that runs while the game_over variable is false,
# i.e., someone hasn't placed 4 in a row yet
while not game_over:

    # for every player event
    for event in pygame.event.get():

        # if player clses the window
        if event.type == pygame.QUIT:
            sys.exit()

        # if player moves the mouse, their piece moves at the top of the screen
        if event.type == pygame.MOUSEMOTION and not_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            xpos = pygame.mouse.get_pos()[0]
            if turn == PLAYER_ONE:
                pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), circle_radius )
            else:
                pygame.draw.circle(screen, YELLOW, (xpos, int(SQUARESIZE/2)), circle_radius )

        # if player clicks the button, we drop their piece down
        if event.type == pygame.MOUSEBUTTONDOWN and not_over:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

            # we assume players will use correct input
            xpos = event.pos[0] 
            col = int(math.floor(xpos/SQUARESIZE)) 

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn)
                if winning_move(board, turn):
                    print(f"PLAYER {turn} WINS!")
                    label = my_font.render(f"PLAYER {turn} WINS!", 1, RED if turn == PLAYER_ONE else YELLOW)
                    screen.blit(label, (40, 10))
                    not_over = False
                    t = Timer(3.0, end_game)
                    t.start()
                
                draw_board(board) 

                # switch turns
                turn = PLAYER_TWO if turn == PLAYER_ONE else PLAYER_ONE

        pygame.display.update()
