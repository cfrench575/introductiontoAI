"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def number_X(board):
    num_X=0
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == X:
                num_X= num_X+1
    return num_X

def number_O(board):
    num_O=0
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == O:
                num_O= num_O+1
    return num_O

def number_empty(board):
    num_empty=0
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == EMPTY:
                num_empty= num_empty+1
    return num_empty


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countempty=number_empty(board)
    mod = countempty % 2
    if mod == 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    row_indices=[]
    col_indices=[]
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell==EMPTY:
                row_indices.append(row_index)
                col_indices.append(col_index)
    possible_actions=set(zip(row_indices, col_indices))
    return possible_actions


#copy_board = deep_copy(board)
#check input, make sure cell is empty, if not raise exception.
#  Make a deep copy of the board, assign x or o depending on player

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board=copy.deepcopy(board)
    row=action[0]
    col=action[1]
    if new_board[row][col] == EMPTY:
        new_board[row][col] = player(board)
    else:
        raise NameError('not a valid action; please choose an empty cell')
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row_index, row in enumerate(board):
        num_X=0
        num_O=0 
        for col_index, cell in enumerate(row):
            if cell == X:
                num_X= num_X+1
            if cell == O:
                num_O= num_O+1
        if num_X == 3:
            return X
        if num_O == 3:
            return O
    for col_index in range(3):
        num_X=0
        num_O=0 
        for row_index in range(3):
            cell=board[row_index][col_index]
            if cell == X:
                num_X= num_X+1
            if cell == O:
                num_O= num_O+1
        if num_X == 3:
            return X
        if num_O == 3:
            return O
    if board[0][0]==X and board[1][1]==X and board[2][2]==X:
        return X
    if board[0][2]==X and board[1][1]==X and board[2][0]==X:
        return X
    if board[0][0]==O and board[1][1]==O and board[2][2]==O:
        return O
    if board[0][2]==O and board[1][1]==O and board[2][0]==O:
        return O
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)==X or winner(board)==O:
        return True
    if number_empty(board)==0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return 1
    if winner(board)==O:
        return -1
    else:
        return 0

#https://github.com/Cledersonbc/tic-tac-toe-minimax/blob/master/py_version/minimax.py
#https://repl.it/talk/learn/Game-Tutorial-Tic-Tac-Toe-Python/8926
#https://www.neverstopbuilding.com/blog/minimax

board=[[X, O, EMPTY],
        [O, X, X],
        [EMPTY, EMPTY, EMPTY]]

board=[['X', 'O', 'X'], ['O', 'X', 'X'], ['O', 'O', None]]

def score(board):
    if terminal(board):
        return utility(board)
    scores=[]
    possible_actions=list(actions(board))
    for action in possible_actions:
        possible_board=result(board, action)
        possible_score=score(possible_board)
        scores.append(possible_score)
        # print(possible_score, action)
    current_player = player(board)
   # print(board)
    #for i in range(len(possible_actions)):
        #print(possible_actions[i], scores[i])
    if current_player == X:
        return max(scores)
    else:
        return min(scores)

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None 
    all_actions=[]
    scores=[]
    current_player=player(board)
    possible_actions=actions(board)
    for action in possible_actions:
        ##ad something in here for alpha beta pruning, for example, if X and 1 is already present in scores list, skip to end
        possible_board=result(board, action)
        possible_score=score(possible_board)
        scores.append(possible_score)
        all_actions.append(action)
    index=0
    if current_player == X:
        index = scores.index(max(scores))
    else:
        index = scores.index(min(scores))
    return all_actions[index]
