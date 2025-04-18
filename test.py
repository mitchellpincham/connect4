import numpy as np

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
        print(diagonal)
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


print(check_win([2, 0, 2, 2, 1, 0, 2, 1, 0, 2, 1, 1, 0, 1, 2, 0, 2, 2, 2, 0, 2, 1, 2, 1, 1, 1, 0, 1, 1, 1, 2, 2, 1, 0, 2, 2, 1, 2, 1, 1, 1, 2]))