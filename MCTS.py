import random
import datetime
import copy
from globals import PLAYER, AI

#  Code was based off of this as a reference https://gitlab.com/dcunhas/
#  Nothing directly copied but most of it is heavily based off of his stuff.


class MCTS():

    def __init__(self):
        self.time = datetime.timedelta(milliseconds=1000)
        self.max = 100
        self.wins = {}
        self.plays = {}
        self.known_states = {}
        self.referenced = False
        self.first_player = ""

    def set_time(self, time):
        self.time = datetime.timedelta(milliseconds=time)

    def get_move(self, game):
        playable_moves = game.playable_moves()
        board = copy.deepcopy(game.board)
        self.first_player = game.first_player
        if not playable_moves:
            return
        elif len(playable_moves) == 1:
            # Only one possibility
            return playable_moves[0]
        player = copy.copy(game.current_player)
        forced_move = game.find_move(player)
        if forced_move != -1:
            return forced_move
        played_games = 0

        begin = datetime.datetime.now()
        while datetime.datetime.now() - begin < self.time:
            self.simulate(game)
            played_games += 1
        moves = [(m, tuple(tuple(col) for col in game.simulate_move(board, m, player))) for m in playable_moves]
        # percent, move = max(
        #     (self.wins[(player, S)] /
        #     self.plays[(player, S)],
        #     m) for m, S in moves
        # )
        percent = -1000
        move = None
        for m, S in moves:
            if (player, S) in self.wins and (player, S) in self.plays:
                temp_percent = self.wins[(player, S)] / self.plays[(player, S)]
                if temp_percent > percent:
                    percent = temp_percent
                    move = m
        if move is None:
            # This means the MCTS didn't have enough time to get to the move.
            move = random.choice(game.playable_moves())
        # print("Percentage for move is ", percent, move)
        return move

    def simulate(self, game):
        memoized = set()
        gamecopy = copy.deepcopy(game)
        player = copy.copy(gamecopy.current_player)
        winner = None
        for i in range(1, self.max + 1):

            playable = gamecopy.playable_moves()
            if not playable:
                break
            # We have to convert the board to a tuple of tuple columns since arrays cant be used for dictionary keys.
            forced = gamecopy.find_move(player)

            move = random.choice(playable)
            if forced != -1:
                move = forced
            valid, win = gamecopy.make_move(move, player)
            if win:
                winner = player
            play_state = (tuple(tuple(col) for col in gamecopy.board))
            if (player, play_state) not in self.plays:
                self.plays[(player, play_state)] = 0
                self.wins[(player, play_state)] = 0
            memoized.add((player, play_state))
            gamecopy.switch_players()
            if self.referenced and play_state in self.known_states:

                if play_state in self.known_states:
                    if self.known_states[play_state] == 1:
                        winner = AI
                    else:
                        winner = PLAYER
                else:
                    winner = copy.copy(gamecopy.current_player)

            player = copy.copy(gamecopy.current_player)
            if winner:
                break
        for played, state in memoized:
            self.plays[(played, state)] += 1
            if played == winner:
                self.wins[(played, state)] += 1
