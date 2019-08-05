from copy import *
import numpy as np
import os
import time

HEIGHT = 6
WIDTH = 7
COLOR = ["X","O"]
MAX = float('inf')
MIN = float('-inf')

def is_playable(state, col):
    if state[0][col] == '#':
        return True
    else:
        print "column is full"
        return False

def drop_coin(state, col, color):
    row = find_height(state, col)
    if row == None:
        row = 5
        state[row][col] = color
    #print row, col
    state[row][col] = color
    return state

def find_height(state, col):
	grid = np.swapaxes(state, 0, 1)
	for row,cell in enumerate(grid[col]):
		if cell == "#":
			continue
        if cell!= "#":
            return row

def move_num(state):
    moves = 0
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if state[row][col].isalpha():
                moves+=1
    #print moves
    return moves

def game_over(grid):
    if find_streak(grid, COLOR[0], 4) > 0:
        return True
    elif find_streak(grid, COLOR[1], 4) > 0:
        return True
    else:
        return False

def evaluate( grid, player_color, depth):

    if player_color == COLOR[0]:
        opp_color = COLOR[1]
    else:
        opp_color = COLOR[0]

    ai_fours = find_streak(grid, player_color, 4)
    ai_threes = find_streak(grid, player_color, 3)
    ai_twos = find_streak(grid, player_color, 2)
    human_fours = find_streak(grid, opp_color, 4)
    human_threes = find_streak(grid, opp_color, 3)
    human_twos = find_streak(grid, opp_color, 2)

    if human_fours > 0:
        return -100000 - depth
    else:
        #print (ai_fours * 100000 + ai_threes * 100 + ai_twos * 10) - (human_threes * 100 + human_twos * 10)

        return (ai_fours * 100000 + ai_threes * 100 + ai_twos * 10) - (human_threes * 100 + human_twos * 10) + depth

def find_streak( grid, color, streak):
    count = 0

    for row in range(HEIGHT):
        for col in range(WIDTH):
            if grid[row][col] == color:

                count += vert_check(row, col, grid, streak)


                count += horz_check(row, col, grid, streak)


                count += diag_check(row, col, grid, streak)

    #print count
    return count

def vert_check( row, col, grid, streak):

    consecutive_item = 0
    if row + streak - 1 < HEIGHT:
        for i in range(streak):
            if grid[row][col] == grid[row + i][col]:
                consecutive_item += 1
            else:
                break

    if consecutive_item == streak:
        return 1
    else:
        return 0

def horz_check( row, col, grid, streak):

    consecutive_item = 0
    if col + streak - 1 < WIDTH:
        for i in range(streak):
            if grid[row][col] == grid[row][col + i]:
                consecutive_item += 1
            else:
                break

    if consecutive_item == streak:
        return 1
    else:
        return 0

def diag_check( row, col, grid, streak):

    total = 0
    consecutive_item = 0
    if row + streak - 1 < HEIGHT and col + streak - 1 < WIDTH:
        for i in range(streak):
            if grid[row][col] == grid[row + i][col + i]:
                consecutive_item += 1
            else:
                break

    if consecutive_item == streak:
        total += 1

    consecutive_item = 0
    if row - streak + 1 >= 0 and col + streak - 1 < WIDTH:
        for i in xrange(streak):
            if grid[row][col] == grid[row - i][col + i]:
                consecutive_item += 1
            else:
                break

    if consecutive_item == streak:
        total += 1

    return total

def minimax_alpha_beta(board, is_max_player, depth, alpha, beta):
    #print "In minmax"
    #maximizing player
    if is_max_player:
        score = evaluate(board, "X", depth)
        if game_over(board) or depth == 6:
            return score
        best_val = float('-inf')
        test_grid = deepcopy(board)
        for i in range(WIDTH):
            if is_playable(test_grid, i):
                drop_coin(test_grid, i, "X")
                best_val = max(best_val,minimax_alpha_beta(test_grid, False, depth+1, alpha, beta))
                alpha = max(alpha, best_val)

                if (beta <= alpha):
                    break
                #Undo the move
                board = matrix
        return best_val
    #minimizing player
    elif not is_max_player:
        score = evaluate(board, "O", depth)
        if game_over(board) or depth == 6:
            return score
        best_val = float('inf')
        test_grid = deepcopy(board)
        for i in range(WIDTH):
            if is_playable(test_grid, i):
                #find_best_move(test_grid,)
                drop_coin(test_grid, i, "O")
                best_val = min(best_val,minimax_alpha_beta(test_grid, True, depth+1, alpha, beta))
                beta = min(best_val, beta)

                if (beta<= alpha):
                    break
                #Undo the move
                board = matrix
        return best_val

def find_best_move(board):
    start_time = time.time()
    alpha = MIN
    best_col = -1
    best_row = -1
    global matrix
    matrix = board

    for col in range(WIDTH):
        if is_playable(board, col):
            grid = drop_coin(board, col, "O")
            #print "dropped"
            move_val = minimax_alpha_beta(grid, True, 0, MIN, MAX)

            if move_val > alpha:
                #print move_val
                best_col = col
                best_row = find_height(board, col)
                if best_row == None:
                    best_row = 5
                alpha = move_val

    print "lemme think for", time.time() - start_time,"seconds"
    return best_row, best_col

def ai_play(board):
    print "Coming up next my move"
    dup_board = deepcopy(board)
    row, col = find_best_move(board)
    dup_board[row][col] = "X"
    board = dup_board
    print_state(board)
    return board

def human_play(board):
    dup_board = deepcopy(board)
    col = input("Enter a column number to play")
    row = find_height(board, col)
    if row == None:
        row = 5
    dup_board[row][col] = "O"
    board = dup_board
    print_state(board)
    return board

def print_state(state):
    for i in range(HEIGHT):
        print("\t"),
        for j in range(WIDTH):
            print("| " + str(state[i][j])),
        print("|")
    print("\t"),

    for k in range(WIDTH):
        print("  %d" % (k)),
    print("")


if __name__ == "__main__":
    #p2 = Connect_Four_Player(board, red)
    board = [['#' for col in range(WIDTH)] for row in range(HEIGHT)]
    print_state(board)
    while not game_over(board):
        game = human_play(board)
        board = ai_play(game)
