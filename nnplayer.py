from keras.optimizers import SGD
from keras.models import load_model
from globals import AI
import numpy as np


class NeuralPlayer():

    def __init__(self):
        self.player = load_model('my_model.h5')        
        sgd = SGD(lr=0.1)
        self.player.compile(loss='mse', optimizer=sgd)

    def get_move(self, board):
        possible = board.playable_moves()
        move_values = []
        for move in possible:
            temp_board = board.simulate_move(board.board, move, AI)
            board_array = [x for col in temp_board for x in col]
            value = self.player.predict(np.array([board_array]))
            move_values.append((value, move))
        return max(move_values, key=lambda x: x[0])[1]
