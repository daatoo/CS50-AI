"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return None

    num = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                num += 1

    return X if num % 2 == 1 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if terminal(board):
        return None

    i, j = action

    if i < 0 or i >= len(board) or j < 0 or j >= len(board[i]):
        raise Exception("Invalid action: out-of-bounds!")

    if board[i][j] != EMPTY:
        raise Exception("Invalid action!")

    copy_board = deepcopy(board)
    current_payer = player(copy_board)
    copy_board[i][j] = current_payer

    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True

    if len(actions(board)) == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)

    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        value, action = max_value(board, float('-inf'), float('inf'))
    else:
        value, action = min_value(board, float('-inf'), float('inf'))

    return action


def max_value(state, alpha, beta):
    if terminal(state):
        return utility(state), None

    v = float('-inf')
    optimal_action = None
    for action in actions(state):
        min_val, _ = min_value(result(state, action), alpha, beta)
        if min_val > v:
            optimal_action = action
            v = min_val
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v, optimal_action


def min_value(state, alpha, beta):
    if terminal(state):
        return utility(state), None

    v = float('inf')
    optimal_action = None
    for action in actions(state):
        max_val, _ = max_value(result(state, action), alpha, beta)
        if max_val < v:
            v = max_val
            optimal_action = action
        beta = v
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v, optimal_action
