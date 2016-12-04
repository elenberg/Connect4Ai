from game import Game
from MCTS import MCTS
from globals import AI, PLAYER
from filereader import FileReader
from nnplayer import NeuralPlayer
import random

g = Game()
game = True
player = PLAYER
mcts = MCTS()
plays = 0
mcts_wins = 0
draws = 0
random_wins = 0
time1 = 20
connect4datareader = FileReader()
connect4datareader.get_data()

NN = NeuralPlayer()

mcts1 = MCTS()
mcts1.known_states = connect4datareader.states_dict
mcts1.referenced = True
mcts1.set_time(time1)
mcts1.first_player = g.first_player
mcts1_wins = 0
nn_wins = 0
plays = 0
game = True
while plays < 100:
        if g.board_full():
            game = False
            g = Game()
        if g.current_player == AI:
                forced = g.find_move(AI)
                move = NN.get_move(g)
                if forced != -1:
                    move = forced
                valid, win = g.make_move(move, AI)
                if win:
                    game = False
                    print("Computer won!")
                    nn_wins += 1
                    g = Game()
                    plays += 1
        else:
            # move = mcts1.get_move(g)
            move = random.choice(g.playable_moves())
            forced = g.find_move(PLAYER)
            if forced != -1:
                move = forced
            valid, win = g.make_move(move, PLAYER)
            if win:
                game = False
                print("MCTS won")
                g = Game()
                plays += 1
                mcts_wins += 1
        g.switch_players()


print(mcts_wins, nn_wins)
