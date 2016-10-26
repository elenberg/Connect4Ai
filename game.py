from globals import BOARD_WIDTH, BOARD_HEIGHT, GAME_CONNECTION, PLAYER, AI
from copy import deepcopy


class Game():

    def __init__(self):
        self.board = [[0.0 for x in range(BOARD_HEIGHT)] for y in range(BOARD_WIDTH)]
        self.heights = [0 for y in range(BOARD_WIDTH)]

    def check_input(self, column):
        # First we need to check if column is a number
        try:
            column = int(column)
        except:
            return False
        # Check if the number exists in the board
        if column < 0 or column >= BOARD_WIDTH:
            return False
        # Check if the column is full.
        if self.heights[column] >= BOARD_HEIGHT:
            return False
        return True

    def check_win_diag_left(self, xpos, ypos):
        # Check if the game is won by a left diagonal
        start_x = xpos
        start_y = ypos
        player = self.board[xpos][ypos]
        while(start_y > 0 and start_x > 0 and player == self.board[start_x - 1][start_y - 1]):
            start_y -= 1
            start_x -= 1
        for i in range(GAME_CONNECTION):
            if not self.check_valid_pos(start_x + i, start_y + i):
                return False
            if self.board[start_x + i][start_y + i] != player:
                return False
        return True

    def check_win_diag_right(self, xpos, ypos):
        # check if the game is won by a right diagonal
        start_x = xpos
        start_y = ypos
        player = self.board[xpos][ypos]
        while(start_y < BOARD_HEIGHT and start_x > 0 and
              player == self.board[start_x - 1][start_y + 1]):
            start_y += 1
            start_x -= 1
        for i in range(GAME_CONNECTION):
            if not self.check_valid_pos(start_x + i, start_y - i):
                return False
            if self.board[start_x + i][start_y - i] != player:
                return False
        return True

    def check_win_column(self, xpos, ypos):
        # Only need to check spaces below.
        # Can't win with a height of 3.
        player = self.board[xpos][ypos]
        if ypos < 3:
            return False
        for i in range(GAME_CONNECTION):
            if not self.check_valid_pos(xpos, ypos - i):
                return False
            if self.board[xpos][ypos - i] != player:
                return False
        return True

    def check_win_row(self, xpos, ypos):
        # First we need to find the starting position for x(the position on the left)
        player = self.board[xpos][ypos]
        start_position = xpos
        while(player == self.board[start_position - 1][ypos] and start_position > 0):
            start_position -= 1
        for i in range(GAME_CONNECTION):
            if not self.check_valid_pos(start_position + i, ypos):
                return False
            if self.board[start_position + i][ypos] != player:
                return False
        return True

    def check_valid_pos(self, xpos, ypos):
        if xpos < 0 or xpos >= BOARD_WIDTH:
            return False
        if ypos < 0 or ypos >= BOARD_HEIGHT:
            return False
        return True

    def check_win(self, xpos, ypos):
        if self.check_win_row(xpos, ypos) or self.check_win_diag_left(xpos, ypos) or\
           self.check_win_column(xpos, ypos) or self.check_win_diag_right(xpos, ypos):
            return True
        return False

    def make_move(self, column, player):
        if not self.check_input(column):
            return False, False
        else:
            self.turn = 1
        column = int(column)
        self.board[column][self.heights[column]] = player
        col_height = self.heights[column]
        self.heights[column] += 1
        if self.check_win(column, col_height):
            return True, True
        return True, False

    def print_board(self):
        for i in reversed(range(BOARD_HEIGHT)):
            for x in range(BOARD_WIDTH):
                print(str(self.board[x][i]) + "\t", end="")
            print()

    def find_move(self, player):
        # Check if there is a win
        original_heights = deepcopy(self.heights)
        original_board = deepcopy(self.board)
        possible_forced = -1
        for i in range(BOARD_WIDTH):
            self.board[i][self.heights[i]] = player
            col_height = self.heights[i]
            self.heights[i] += 1
            if self.check_win(i, col_height):
                self.board = deepcopy(original_board)
                self.heights = deepcopy(original_heights)
                return i
            self.board = deepcopy(original_board)
            self.heights = deepcopy(original_heights)
            temp_player = player
            if temp_player == PLAYER:
                temp_player = AI
            else:
                temp_player = PLAYER
            self.board[i][self.heights[i]] = temp_player
            col_height = self.heights[i]
            self.heights[i] += 1
            if self.check_win(i, col_height):
                self.board = deepcopy(original_board)
                self.heights = deepcopy(original_heights)
                possible_forced = i
            self.board = deepcopy(original_board)
            self.heights = deepcopy(original_heights)
        if possible_forced > -1:
            return possible_forced
        else:
            return -1

g = Game()
game = True
player = PLAYER
while game:
    g.print_board()
    possible = g.find_move(player)
    if possible != -1:
        print("Move into column ", possible, " is advised")
    if player == PLAYER:
        print("Player 1 to move")
    else:
        print("Player 2 to move")
    column = input("Input a column number (0-6)")
    valid, win = g.make_move(column, player)
    while not valid:
        column = input("Input a column number (0-6)")
        valid, win = g.make_move(column, player)
    if win:
        game = False
        print(player, "Wins!")
    if player == PLAYER:
        player = AI
    else:
        player = PLAYER
g.print_board()
