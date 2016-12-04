from game import Game
from MCTS import MCTS
from globals import AI, PLAYER
from filereader import FileReader
import random

g = Game()
game = True
player = PLAYER
mcts = MCTS()
plays = 0
mcts_wins = 0
draws = 0
random_wins = 0
time1 = 100
connect4datareader = FileReader()
connect4datareader.get_data()

mcts1 = MCTS()
mcts2 = MCTS()
mcts1.known_states = connect4datareader.states_dict
mcts1.referenced = True
mcts2.known_states = connect4datareader.states_dict
mcts2.referenced = False
time2 = 0
with open("100mcsvsrand.txt", 'a') as file_open:
    # while time1 <= 1000 or time2 == 0:
    #     plays = 0
    #     time2 += 100
    #     if time2 > 1000:
    #         time1 += 100
    #         time2 = 100
    #     mcts1.set_time(time1)
    #     mcts2.set_time(time2)
    #     mcts1.first_player = g.first_player
    #     mcts2.first_player = g.first_player
    #     mcts1_wins = 0
    #     mcts2_wins = 0
    #     draws = 0
    while time1 <= 1000:
        mcts1.set_time(time1)
        mcts1.first_player = g.first_player
        mcts1_wins = 0
        mcts2_wins = 0
        plays = 0
        while game and plays < 100:
            print('plays ', plays, end='\r')
            if g.current_player == AI:
                move = mcts1.get_move(g)
                valid, win = g.make_move(move, AI)
                if win:
                    mcts1_wins += 1
                    plays += 1
                    g = Game()
            else:
                forced = g.find_move(PLAYER)
                playable = g.playable_moves()
                move = random.choice(playable)
                if forced != -1:
                    move = forced
                valid, win = g.make_move(move, PLAYER)
                if win:
                    plays += 1
                    g = Game()
            g.switch_players()
            if g.board_full():
                draws += 1
                plays += 1
                g = Game()
        time1 += 100
        file_open.write(str(time1) + '\t' + str(mcts1_wins / (plays)) + '\n')
        file_open.flush()
        print(str(time1) + '\t' + str(mcts1_wins / (plays)) + '\n')

        