from globals import BOARD_WIDTH, BOARD_HEIGHT, GAME_CONNECTION, PLAYER, AI
from copy import deepcopy
from random_ai import RandomAI
import random
from MCTS import MCTS


class Game():

    def __init__(self):
        self.board = [[0 for x in range(BOARD_HEIGHT)] for y in range(BOARD_WIDTH)]
        self.heights = [0 for y in range(BOARD_WIDTH)]
        self.last_error = ""
        self.players = [AI, PLAYER]
        self.current_player = AI
        self.first_player = AI

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
        while(start_y < BOARD_HEIGHT - 1 and start_x > 1 and
              player == self.board[start_x - 1][start_y + 1]):
            start_y += 1
            start_x -= 1
        for i in range(GAME_CONNECTION):
            if not self.check_valid_pos(start_x + i, start_y - i):
                return False
            try:
                if self.board[start_x + i][start_y - i] != player:
                    return False
            except Exception as e:
                import ipdb; ipdb.set_trace()   
        return True

    def find_current_player_from_board(board):
        countai = 0
        countplayer = 0
        for col in board:
            for i in col:
                if i == AI:
                    countai += 1
                elif i == PLAYER:
                    countplayer += 1
        if countai == countplayer:
            return AI
        elif countai > countplayer:
            return PLAYER
        else:
            return AI

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
        column = int(column)
        self.board[column][self.heights[column]] = player
        col_height = self.heights[column]
        self.heights[column] += 1
        return True, self.check_win(column, col_height)

    def print_board(self):
        for i in reversed(range(BOARD_HEIGHT)):
            for x in range(BOARD_WIDTH):
                print("\t" + str(self.board[x][i]), end="")
            print()
        for x in range(BOARD_WIDTH):
            print("\t_", end="")
        print()
        for x in range(BOARD_WIDTH):
            print("\t" + str(x), end="")
        print()

    def board_full(self):
        for height in self.heights:
            if height < BOARD_HEIGHT:
                return False
        return True

    def find_move(self, player):
        # Check if there is a win
        original_heights = deepcopy(self.heights)
        original_board = deepcopy(self.board)
        possible_forced = -1
        for i in range(BOARD_WIDTH):
            if self.heights[i] < BOARD_HEIGHT:
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

    def playable_moves(self):
        playable = []
        for i in range(len(self.heights)):
            if self.heights[i] < BOARD_HEIGHT:
                playable.append(i)
        return playable

    def switch_players(self):
        if self.current_player == AI:
            self.current_player = PLAYER
        else:
            self.current_player = AI

    def generate_heights_from_board(self, board):
        heights_to_return = [-1 for y in range(0, BOARD_WIDTH)]
        for i in range(0, BOARD_WIDTH):
            for x in range(0, BOARD_HEIGHT):
                if heights_to_return[i] == -1 and board[i][x] == 0:
                    heights_to_return[i] = x
        for i in range(BOARD_WIDTH):
            if heights_to_return[i] == -1:
                heights_to_return = BOARD_HEIGHT
        return heights_to_return

    def simulate_move(self, board, column, player):
        boardcopy = deepcopy(board)
        for i in range(0, BOARD_HEIGHT):
            if boardcopy[column][i] == 0.0:
                boardcopy[column][i] = player
                return boardcopy
        return boardcopy

    def get_last_move_from_board(board):
        countai = 0
        countplayer = 0
        for col in board:
            for i in col:
                if i == AI:
                    countai += 1
                elif i == PLAYER:
                    countplayer += 1
        if countai == countplayer:
            return PLAYER
        else:
            return AI
# g = Game()
# game = True
# player = PLAYER
# ai = RandomAI()
# mcts = MCTS()
# plays = 0
# mcts_wins = 0
# draws = 0
# random_wins = 0
# while game and plays < 1000:
#     if g.current_player == AI:
#         move = mcts.get_move(g)
#         valid, win = g.make_move(move, AI)
#         if win:
#             mcts_wins += 1
#             plays += 1
#             g = Game()
#             print("MCT won", mcts_wins)
#     else:
#         forced = g.find_move(PLAYER)
#         move = random.choice(g.playable_moves())
#         if forced != -1:
#             move = forced
#         valid, win = g.make_move(move, PLAYER)
#         if win:
#             random_wins += 1
#             plays += 1
#             g = Game()
#             print("Random won", random_wins)
#     g.switch_players()
#     if g.board_full():
#         draw += 1
#         plays += 1
#         g = Game()
# print("MCTS wins", mcts_wins)
# print("random_wins", random_wins)
# print("draws", draws)
# # if(input("Play against ai? Press 1 for Random AI, 0 for 2 players") == '1'):
# #     while game:
# #         # AI will go first.

# #         ai_forced = g.find_move(AI)
# #         if ai_forced != -1:
# #             valid, win = g.make_move(ai_forced, AI)
# #             if win:
# #                 print("RandomAI won")
# #                 game = False
# #                 break
# #         else:
# #             valid, win = g.make_move(ai.get_random_move(g.playable_moves()), AI)
# #             if win:
# #                 print("RandomAI won")
# #                 game = False
# #                 break
# #         g.print_board()
# #         print("Player to move")
# #         column = input("Input a column number (0-6)")
# #         valid, win = g.make_move(column, PLAYER)
# #         while not valid:
# #             column = input("Input a column number (0-6)")
# #             valid, win = g.make_move(column, PLAYER)
# #         if win:
# #             game = False
# #             print(PLAYER, "Wins!")

# # else:
# #     while game:
# #         g.print_board()
# #         possible = g.find_move(player)
# #         if possible != -1:
# #             print("Move into column ", possible, " is advised")
# #         if g.board_full():
# #             print("Board is full. Game is tied.")
# #             break
# #         if player == PLAYER:
# #             print("Player 1 to move")
# #         else:
# #             print("Player 2 to move")
# #         column = input("Input a column number (0-6)")
# #         valid, win = g.make_move(column, player)
# #         while not valid:
# #             column = input("Input a column number (0-6)")
# #             valid, win = g.make_move(column, player)
# #         if win:
# #             game = False
# #             print(player, "Wins!")
# #         if player == PLAYER:
# #             player = AI
# #         else:
# #             player = PLAYER
# g.print_board()
