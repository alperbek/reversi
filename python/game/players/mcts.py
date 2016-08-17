from player import Player
import time
import random
from math import log, sqrt


class MonteCarloTreeSearchPlayer(Player):
    def __init__(self, max_seconds):
        self._max_seconds = max_seconds
        self._c = sqrt(2.0)  # theoretically sqrt(2); in practice usually chosen empirically
        self._wins = {}
        self._plays = {}

    def decide(self, context):
        valid_actions = context.get_valid_actions()
        if len(valid_actions) == 0:
            return None

        start = time.time()
        while time.time() - start < self._max_seconds:
            self._simulate(context)

        _, best_action = max([(self._win_ratio(context.apply(action)), action)
                              for action in valid_actions])
        return best_action

    def _win_ratio(self, context):
        return self._wins.get(context, 0.0) / self._plays.get(context, 1.0)

    def _ucb1(self, contexts):
        log_sum = log(sum(self._plays[c] for c in contexts))
        _, best_context = max([(self._win_ratio(c) + self._c * sqrt(log_sum / self._plays[c]), c)
                               for c in contexts])
        return best_context

    def _simulate(self, context):
        visited = set()
        expand = True
        winner = None

        while context.is_active():
            # selection of action (aka context)
            valid_actions = context.get_valid_actions()
            if len(valid_actions) > 0:
                contexts = [context.apply(action) for action in valid_actions]
                if all(self._plays.get(c) for c in contexts):
                    # exploitation based on UCB1
                    context = self._ucb1(contexts)
                else:
                    # exploration
                    context = random.choice(contexts)
            else:
                context = context.apply(None)  # pass to the opponent

            # expansion of tree / node
            if expand and context not in self._plays:
                expand = False
                self._plays[context] = 0.0
                self._wins[context] = 0.0

            visited.add(context)

            if context.is_winner():
                winner = context.get_player()
                break

        # back propagation of wins / plays
        for context in visited:
            if context in self._plays:
                self._plays[context] += 1.0
                if context.get_player() == winner:
                    self._wins[context] += 1.0
