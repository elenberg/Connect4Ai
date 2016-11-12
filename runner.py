from game import Game
from MCTS import MCTS
from globals import AI, PLAYER
from filereader import FileReader

g = Game()
game = True
player = PLAYER
mcts = MCTS()
plays = 0
mcts_wins = 0
draws = 0
random_wins = 0
time1 = 250
connect4datareader = FileReader()
connect4datareader.get_data()

mcts1 = MCTS()
mcts2 = MCTS()
mcts1.known_states = connect4datareader.states_dict
mcts1.referenced = False
mcts2.known_states = connect4datareader.states_dict
mcts2.referenced = False
time2 = 0
with open("results_states3.txt", 'a') as file_open:
    while time1 <= time2 or time2 == 0:
        plays = 0
        time2 += 250
        if time2 > 2000:
            time1 += 250
            time2 = time1
        mcts1.set_time(time1)
        mcts2.set_time(time2)
        mcts1.first_player = g.first_player
        mcts2.first_player = g.first_player
        mcts1_wins = 0
        mcts2_wins = 0
        draws = 0
        while game and plays < 100:
            if g.current_player == AI:
                move = mcts1.get_move(g)
                valid, win = g.make_move(move, AI)
                if win:
                    mcts1_wins += 1
                    plays += 1
                    g = Game()
            else:
                forced = g.find_move(PLAYER)
                move = mcts2.get_move(g)
                valid, win = g.make_move(move, PLAYER)
                if win:
                    mcts2_wins += 1
                    plays += 1
                    g = Game()
            g.switch_players()
            if g.board_full():
                draws += 1
                plays += 1
                g = Game()
        file_open.write(str(time1) + '\t' + str(time2) + '\t' + str(mcts1_wins / (plays)) + '\n')
        file_open.flush()
        print(str(time1) + '\t' + str(time2) + '\t' + str(mcts1_wins / (plays)) + '\n')

        