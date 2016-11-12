from globals import AI, PLAYER, BOARD_WIDTH, BOARD_HEIGHT


class FileReader():

    def __init__(self):
        self.states_dict = {}

    def get_data(self):
        with open('connect.data', 'r') as fileopen:
            for line in fileopen.readlines():
                solutions = line.split(',')
                board = [[0 for y in range(BOARD_HEIGHT)] for x in range(BOARD_WIDTH)]
                for i in range(0, BOARD_WIDTH):
                    for x in range(0, BOARD_HEIGHT):
                        temp = solutions[i * BOARD_HEIGHT + x]
                        if temp is 'x':
                            temp = AI
                        elif temp is 'o':
                            temp = PLAYER
                        else:
                            temp = 0
                        board[i][x] = temp
                board_tuple = (tuple(tuple(col) for col in board))
                self.states_dict[board_tuple] = 0
                if solutions[len(solutions) - 1].strip() is 'win':
                    self.states_dict[board_tuple] = 1
