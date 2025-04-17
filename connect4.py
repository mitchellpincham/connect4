import pygame
import sys
import numpy as np
import random

CELL_SIZE:int = 150
WIDTH:int = CELL_SIZE * 7
HEIGHT:int = CELL_SIZE * 6
DEPTH:int = 7

pygame.init()
screen:pygame.Surface = pygame.display.set_mode([WIDTH, HEIGHT])


# 0 = empty, 1 = player 1, 2 = player 2.
board:np.ndarray = np.zeros(42)


def check_win(board:np.ndarray) -> int:
    """
    Add two numbers and return the result.

    Args:
        board, a list of integers, each int in range [0, 2]. The list should be length 42

    Returns:
        int of who's won, in range [0, 2]
    """

    # check rows
    for y in range(5, -1, -1):
        row = board[y * 7: y * 7 + 7]  # get a slice of the row
        
        if (row[3] == 0): continue

        for i in range(4):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                return row[i]
            

    # check columns
    for x in range(7):
        column = board[x::7]  # rows with index = x mod 7, ie. the column

        if column[2] == 0 or column[3] == 0: continue

        for i in range(3):
            if column[i] == column[i + 1] == column[i + 2] == column[i + 3]:
                return column[i]

    # check diagonals, check like the columns, but each row is right by 1
    """ 
        0123456
        7012345
        6701234
        5670123
        4567012
        3456701
    """
    # 4, 5 cannot have 4 in an row; 
    # 3, 6 are tricky as they wrap around, so we have to slice those cases.
    diagonal = board[3::8][:4]
    if np.all(diagonal):
        return diagonal[0]
    
    diagonal = board[6::8][1:]
    if np.all(diagonal):
        return diagonal[0]
    
    for x in [0, 1, 2, 6, 7]:
        diagonal = board[x::8]

        if diagonal[2] == 0 or diagonal[3] == 0: continue

        for i in range(len(diagonal) - 3):
            if diagonal[i] == diagonal[i + 1] == diagonal[i + 2] == diagonal[i + 3]:
                return diagonal[i]
            

    # Now for the other diagonals, we choose index mod 6
    """
        0123450
        1234501
        2345012
        3450123
        4501234
    """
    # 0, 1, 2 need the front sliced off
    for x in [0, 1, 2]:
        diagonal = board[x::6][x + 1:]

        if diagonal[2] == 0 or diagonal[3] == 0: continue

        for i in range(len(diagonal) - 3):
            if diagonal[i] == diagonal[i + 1] == diagonal[i + 2] == diagonal[i + 3]:
                return diagonal[i]
    
    # 3, 4, 5 need the end sliced off
    for x in [3, 4, 5]:
        diagonal = board[x::6][:x + 1]

        if diagonal[2] == 0 or diagonal[3] == 0: continue

        for i in range(len(diagonal) - 3):
            if diagonal[i] == diagonal[i + 1] == diagonal[i + 2] == diagonal[i + 3]:
                return diagonal[i]


def get_colour(player:int) -> pygame.Color:
    if player == 0:
        return pygame.Color(255, 255, 255)
    if player == 1:
        return pygame.Color(230, 20, 50)
    #if player == 2:
    return pygame.Color(250, 180, 30)


def play(pos:int, player:int) -> bool:
    pos += 35

    # replace with [y for y in x if y % 2 == 0] logic

    while pos >= 0:
        if board[pos] == 0:
            board[pos] = player
            return True
        pos -= 7

    return False


def possible_moves(board:list[int]) -> list[int]:
    #options = [1 if val == 0 else 0 for val in top_row]
    return [i for i in range(len(board[:7])) if board[i] == 0]


def make_move(old_board:list[int], pos:int, player:int) -> list[int]:
    pos += 35

    # replace with [y for y in x if y % 2 == 0] logic

    new_board = old_board.copy()

    while pos >= 0:
        if new_board[pos] == 0:
            new_board[pos] = player
            return new_board
        pos -= 7



def minimax(board:list[int], depth:int, alpha, beta, maximising_ai):
    if depth == 0:
        # get value somehow
        return 0
    
    options = possible_moves(board)
    if len(options) == 0:
        return 0  # draw
    
    win = check_win(board)
    if win:
        if win == 1:
            return -100 - depth  # player win
        else:
            return 100 + depth  # ai win

    
    if maximising_ai:
        bestValue = -np.inf
        for move in options:
            child = make_move(board, move, 2)

            value = minimax(child, depth - 1, alpha, beta, False)
            bestValue = max(bestValue, value)
            if bestValue >= beta:
                break
            alpha = max(alpha, bestValue)

        return bestValue

    else:
        bestValue = np.inf
        for move in options:
            child = make_move(board, move, 1)

            value = minimax(child, depth - 1, alpha, beta, True)
            bestValue = min(bestValue, value)
            if bestValue <= alpha:
                break
            beta = min(beta, value)
        return bestValue


def ai_play(board:list[int]) -> list[int]:
    # get all the options

    top_row = board[:7]

    #options = [1 if val == 0 else 0 for val in top_row]
    options = [i for i in range(len(top_row)) if top_row[i] == 0]

    # board full, draw
    if len(options) == 0:
        return board

    best_value = -np.inf
    best_moves = [0]
    for option in options:

        child = make_move(board, option, 2)

        value = minimax(child, DEPTH, -np.inf, np.inf, False)
        print(option, value)
        if value > best_value:
            best_value = value
            best_moves = [option]
        elif value == best_value:
            best_moves.append(option)

    return make_move(board, random.choice(best_moves), 2)

    
    




while True:
    screen.fill([0, 0, 0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x:int = pygame.mouse.get_pos()[0]

            cell_x:int = mouse_x // CELL_SIZE
            cell_x = max(0, cell_x)
            cell_x = min(6, cell_x)

            if play(cell_x, 1):
                board = ai_play(board)

            print(check_win(board))


    
    for i, cell in enumerate(board):
        x:int = (i % 7) * CELL_SIZE + CELL_SIZE / 2
        y:int = i // 7 * CELL_SIZE + CELL_SIZE / 2

        colour:pygame.Color = get_colour(cell)

        pygame.draw.circle(screen, colour, [x, y], CELL_SIZE / 2.1)
        

    pygame.display.flip()
