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
time1 = 3000
connect4datareader = FileReader()
connect4datareader.get_data()

mcts1 = MCTS()
mcts2 = MCTS()
mcts1.known_states = connect4datareader.states_dict
mcts1.referenced = False
mcts1.set_time(time1)
mcts1.first_player = g.first_player
mcts1_wins = 0
mcts2_wins = 0
plays = 0
game = True
computer_last_turn = 0
while game:
        if g.board_full():
            print("Board is full. Game is tied.")
            game = False
            break
        if g.current_player == AI:
                print("Computer is thinking and making its move.")
                move = mcts1.get_move(g)
                valid, win = g.make_move(move, AI)
                computer_last_turn = move
                if win:
                    game = False
                    print("Computer won!")
                    g.print_board()
        else:
            print(chr(27) + "[2J")
            g.print_board()
            print("Player to move. You are", PLAYER)
            print("Computer played in column " + str(computer_last_turn) + " last turn")
            column = input("Input a column number (0-6)")
            valid, win = g.make_move(column, player)
            while not valid:
                column = input("Input a column number (0-6)")
                valid, win = g.make_move(column, player)
            if win:
                game = False
                print(player, "Wins!")
        g.switch_players()
