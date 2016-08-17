from player import Player
import random


class RandomPlayer(Player):
    def decide(self, context):
        actions = context.get_valid_actions()
        if len(actions) == 0:
            return None
        return random.choice(actions)
