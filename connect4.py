import pygame
import sys
import numpy as np
import random

global visited_states
visited_states:set = set()

CELL_SIZE:int = 150
WIDTH:int = CELL_SIZE * 7
HEIGHT:int = CELL_SIZE * 6
DEPTH:int = 8
SEARCH_ORDER:list[int] = [3, 2, 4, 1, 5, 0, 6]

pygame.init()
screen:pygame.Surface = pygame.display.set_mode([WIDTH, HEIGHT])

# 0 = empty, 1 = player 1, 2 = player 2.
board:np.ndarray = np.zeros(42)

def check_win(board:np.ndarray) -> int:
    """
    Add two numbers and return the result.

    Args:
        board: a list of integers, each int in range [0, 2]. The list should be length 42

    Returns:
        int: who's won, in range [0, 2]
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
    if diagonal[0] != 0 and (diagonal[0] == diagonal[1] == diagonal[2] == diagonal[3]):
        return diagonal[0]
    
    diagonal = board[6::8][1:]
    if diagonal[0] != 0 and (diagonal[0] == diagonal[1] == diagonal[2] == diagonal[3]):
        return diagonal[0]
    
    for x in [0, 1, 2, 7]:
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
        5012345
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
    """
    Get the player's colours for drawing the circles

    Args:
        player: which player

    Returns:
        pygame colour object of which colour to draw
    """
    if player == 0:
        return pygame.Color(255, 255, 255)
    if player == 1:
        return pygame.Color(230, 20, 50)
    #if player == 2:
    return pygame.Color(250, 180, 30)


def hash_board(board:list[int]) -> str:
    """
    Creates a more compact hash of the board

    Args:
        board: The current board

    Returns:
        Doesn't matter the type as it's just getting added to set, whatevers convenient
    """

    return ''.join(map(str, board))


def possible_moves(board:list[int]) -> list[int]:
    """
    Gives us an array of the possible moves of a given board, ie. the top counter is empty

    Args:
        board: The board to check

    Returns:
        An array integers from 0 to 6, for each column that can be played.
    """
    return [i for i in SEARCH_ORDER if board[i] == 0]


def make_move(old_board:list[int], pos:int, player:int) -> list[int]:
    """
    Create the next state after the given move is made

    Args:
        old_board: The board to be played
        pos: Where to play
        player: Which colour to play

    Returns:
        The updated board
    """
    # start at the bottom of the board
    pos += 35

    new_board = old_board.copy()

    # move up the column
    while pos >= 0:
        if new_board[pos] == 0:
            new_board[pos] = player
            return new_board
        pos -= 7

    # if we're at the top
    return old_board


def minimax(board:list[int], depth:int, alpha:float, beta:float, player:int):
    """
    A Negamax implimentation of minimax with Alpha-Beta pruning
    Args:
        board: the game board
        depth: How many more recursions to go
        alpha:
        beta:
        player: which player is playing, swaps between 1 and 2 for each recusion step
    Returns:
    
    """
    
    win = check_win(board)
    if win:
        if win == player:
            return depth
        else:
            return -depth

    if depth == 0:
        # get value somehow
        return 0
    
    options = possible_moves(board)
    if len(options) == 0:
        return 0  # draw
    
    max_value = -np.inf
    for move in options:
        child = make_move(board, move, player)

        hashed_child = hash_board(child)

        if hashed_child in visited_states:
            continue

        visited_states.add(hashed_child)
        value = -minimax(child, depth - 1, -beta, -alpha, (player % 2) + 1)

        if value >= beta: return value
        max_value = max(max_value, value)
        alpha = max(alpha, value)

    return max_value


def ai_play(board:list[int]) -> list[int]:
    """
    Find the best move for the ai, return the board with the given move

    Args:
        board: The game board
    Returns:
        The updated board
    """

    visited_states.clear()
    options = possible_moves(board)

    best_value = -np.inf
    best_move = 0
    for option in options:

        child = make_move(board, option, 2)

        value = -minimax(child, DEPTH, -np.inf, np.inf, 1)
        print(option, value)
        if value > best_value:
            best_value = value
            best_move = option

    return make_move(board, best_move, 2)


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

            possible_move = possible_moves(board)
            if len(possible_move) == 0 or check_win(board) or cell_x not in possible_move:
                continue


            board = make_move(board, cell_x, 1)
            
            if not check_win(board):
                board = ai_play(board)

            if check_win(board):
                print(check_win(board))
                print(board)


    for i, cell in enumerate(board):
        x:int = (i % 7) * CELL_SIZE + CELL_SIZE / 2
        y:int = i // 7 * CELL_SIZE + CELL_SIZE / 2

        colour:pygame.Color = get_colour(cell)

        pygame.draw.circle(screen, colour, [x, y], CELL_SIZE / 2.1)
        

    pygame.display.flip()
