import os
import random
import time

GRID_WIDTH = 7
GRID_HEIGHT = 6
COLOR = ["X", "O"]
MIN = float('-inf')

class Player(object):
    _type = None
    _color = None

    def __init__(self, color):
        self._color = color

class Human_player(Player):
    def __init__(self, color):
        super(Human_player, self).__init__(color)
        self._type = "Human"

    def get_move(self, grid):
        # It returns the column corresponding to the move of human
        column = None
        while column == None:
            try:
                column = int(raw_input("Don't make me wait enter a column number : "))
            except ValueError:
                column = None
            if column >=0 or column <= 6:
                return column
            else:
                column = None

class Computer_player(Player):
    depth = 5

    def __init__(self, color):
        super(Computer_player, self).__init__(color)
        self._type = "Computer"

    def get_move(self, grid):
        return self.find_best_move(grid)

    def find_best_move(self, grid):
        start_time = time.time()
        print "AI is thinking!!...."
        # determine opponent's color
        if self._color == COLOR[0]:
            human_color = COLOR[1]
        else:
            human_color = COLOR[0]

        playable_moves = {}

        for col in xrange(GRID_WIDTH):
            if self.is_playable(col, grid):
                dup_board = self.drop_coin(grid, col, self._color)
                playable_moves[col] = -self.minimax(self.depth - 1, dup_board, human_color)
        best_alpha = MIN
        best_move = None
        moves = playable_moves.items()
        # search for the best move
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        print "lemme think for", time.time() - start_time,"seconds"

        return best_move

    def minimax(self, depth, grid, curr_player_color):
        # returns best value or best score
        playable_moves = []
        for i in xrange(GRID_HEIGHT):
            if self.is_playable(i, grid):
                dup_board = self.drop_coin(grid, i, curr_player_color)
                playable_moves.append(dup_board)

        if depth == 0 or len(playable_moves) == 0 or self.is_win(grid):
            return self.evaluate(depth, grid, curr_player_color)

        if curr_player_color == COLOR[0]:
            opp_player_color = COLOR[1]
        else:
            opp_player_color = COLOR[0]

        best_val = MIN
        for child in playable_moves:
            if child == None:
                print("done")
            best_val = max(best_val, -self.minimax(depth - 1, child, opp_player_color))
        return best_val

    def is_playable(self, column, grid):
        for i in xrange(GRID_HEIGHT - 1, -1, -1):
            if grid[i][column] == '_':

                return True

        #the column is full
        return False

    def is_win(self, grid):
        if self.find_streak(grid, COLOR[0], 4) > 0:
            return True
        elif self.find_streak(grid, COLOR[1], 4) > 0:
            return True
        else:
            return False

    def drop_coin(self, grid, column, color):
        dup_board = [x[:] for x in grid]
        for i in xrange(GRID_HEIGHT - 1, -1, -1):
            if dup_board[i][column] == '_':
                dup_board[i][column] = color
                return dup_board

    def evaluate(self, depth, grid, player_color):
        if player_color == COLOR[0]:
            opp_color = COLOR[1]
        else:
            opp_color = COLOR[0]

        ai_fours = self.find_streak(grid, player_color, 4)
        ai_threes = self.find_streak(grid, player_color, 3)
        ai_twos = self.find_streak(grid, player_color, 2)
        human_fours = self.find_streak(grid, opp_color, 4)
        human_threes = self.find_streak(grid, opp_color, 3)
        human_twos = self.find_streak(grid, opp_color, 2)

        if human_fours > 0:
            return -100000 - depth
        else:
            return (ai_fours * 100000 + ai_threes * 100 + ai_twos * 10) - (human_threes * 100 + human_twos * 10) + depth

    def find_streak(self, grid, color, streak):
        count = 0

        for i in xrange(GRID_HEIGHT):
            for j in xrange(GRID_WIDTH):
                if grid[i][j] == color:
                    count += self.vertical_check(i, j, grid, streak)
                    count += self.horizontal_check(i, j, grid, streak)
                    count += self.diagonal_check(i, j, grid, streak)
        return count

    def vertical_check(self, row, col, grid, streak):
        consecutive_item = 0
        if row + streak - 1 < GRID_HEIGHT:
            for i in xrange(streak):
                if grid[row][col] == grid[row + i][col]:
                    consecutive_item += 1
                else:
                    break

        if consecutive_item == streak:
            return 1
        else:
            return 0

    def horizontal_check(self, row, col, grid, streak):
        consecutive_item = 0
        if col + streak - 1 < GRID_WIDTH:
            for i in xrange(streak):
                if grid[row][col] == grid[row][col + i]:
                    consecutive_item += 1
                else:
                    break

        if consecutive_item == streak:
            return 1
        else:
            return 0

    def diagonal_check(self, row, col, grid, streak):
        total = 0

        consecutive_item = 0
        if row + streak - 1 < GRID_HEIGHT and col + streak - 1 < GRID_WIDTH:
            for i in xrange(streak):
                if grid[row][col] == grid[row + i][col + i]:
                    consecutive_item += 1
                else:
                    break

        if consecutive_item == streak:
            total += 1

        consecutive_item = 0
        if row - streak + 1 >= 0 and col + streak - 1 < GRID_WIDTH:
            for i in xrange(streak):
                if grid[row][col] == grid[row - i][col + i]:
                    consecutive_item += 1
                else:
                    break

        if consecutive_item == streak:
            total += 1

        return total

class Game(object):
    board_width = GRID_WIDTH
    board_height = GRID_HEIGHT
    board = None
    number_of_moves = None
    completed = False
    winner = None
    current_player = None
    players = [None, None]
    colors = COLOR

    def __init__(self):

        # init players with their "colors"
        self.players[0] = Human_player(self.colors[0])
        self.players[1] = Computer_player(self.colors[1])

    def start_game(self):
        #initializing the game
        self.number_of_moves = 1
        self.completed = False
        self.winner = None
        # change to make the human player play first
        self.current_player = self.players[1]
        # create an empty grid
        self.board = list()
        for height in xrange(self.board_height):
            self.board.append([])
            for width in xrange(self.board_width):
                self.board[height].append('_')
        while not self.completed:
            self.next_move()

    def switch_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def next_move(self):
        # get the "move" (column) that the player played
        column = self.current_player.get_move(self.board)
        # search the available line in the selected column
        for i in xrange(self.board_height - 1, -1, -1):
            if self.board[i][column] == '_':
                # set the color in the grid
                self.board[i][column] = self.current_player._color
                if self.number_of_moves > self.board_width * self.board_height:
                    self.completed = True
                if self.game_over():
                    self.completed = True
                    self.winner = self.current_player
                self.print_board()
                # switch the player
                if self.current_player == self.players[0]:
                    self.current_player = self.players[1]
                else:
                    self.current_player = self.players[0]

                self.number_of_moves += 1
                return
        print("Err, according to my calculations this column is full")
        return

    def game_over(self):
        for row in xrange(self.board_height - 1, -1, -1):
            for col in xrange(self.board_width):
                if self.board[row][col] != '_':

                    if self.four_in_column(row, col):
                        return True
                    # verify for horizontal connect
                    if self.four_in_row(row, col):
                        return True
                    # verify for diagonal connect
                    if self.four_in_diagonal(row, col):
                        return True

        return False

    def four_in_column(self, row, col):
        connected_coins = 0

        if row + 3 < self.board_height:
            for i in xrange(4):
                if self.board[row][col] == self.board[row + i][col]:
                    connected_coins += 1
                else:
                    break

            if connected_coins == 4:
                if self.players[0]._color == self.board[row][col]:
                    self.winner = self.players[0]
                else:
                    self.winner = self.players[1]
                return True

        return False

    def four_in_row(self, row, col):
        connected_coins = 0

        if col + 3 < self.board_width:
            for i in xrange(4):
                if self.board[row][col] == self.board[row][col + i]:
                    connected_coins += 1
                else:
                    break

            if connected_coins == 4:
                if self.players[0]._color == self.board[row][col]:
                    self.winner = self.players[0]
                else:
                    self.winner = self.players[1]
                return True

        return False

    def four_in_diagonal(self, row, col):
        connected_coins = 0
        # primary diagonal
        if row + 3 < self.board_height and col + 3 < self.board_width:
            for i in xrange(4):
                if self.board[row][col] == self.board[row + i][col + i]:
                    connected_coins += 1
                else:
                    break

            if connected_coins == 4:
                if self.players[0]._color == self.board[row][col]:
                    self.winner = self.players[0]
                else:
                    self.winner = self.players[1]
                return True

        connected_coins = 0
        # secondary diagonal
        if row - 3 >= 0 and col + 3 < self.board_width:
            for i in xrange(4):
                if self.board[row][col] == self.board[row - i][col + i]:
                    connected_coins += 1
                else:
                    break

            if connected_coins == 4:
                if self.players[0]._color == self.board[row][col]:
                    self.winner = self.players[0]
                else:
                    self.winner = self.players[1]
                return True

        return False

    def print_board(self):

        # prints the current Round
        print("Move number: " + str(self.number_of_moves))
        print("")
        # prints the grid
        for i in xrange(self.board_height):
            print(""),
            for j in xrange(self.board_width):
                print("| " + str(self.board[i][j])),
            print("|")
        print(" "),
        for k in xrange(self.board_width):
            print("  %d" % (k)),
        print("")
        # print final message
        if self.completed:
            print("Aww!! better luck next time")
            if self.winner == None:
                print("Looks like you are smart after all")

if __name__ == "__main__":
    connect4 = Game()
    connect4.start_game()
