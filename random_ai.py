import random


class RandomAI():

    def __init__(self):
        self.wins = 0

    def get_random_move(self, allowed_moves):
        return random.choice(allowed_moves)
