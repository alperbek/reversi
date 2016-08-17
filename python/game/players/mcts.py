from player import Player
import time


class MonteCarloTreeSearchPlayer(Player):
    def __init__(self, max_seconds):
        self._max_seconds = max_seconds

    def decide(self, context):
        start = time.time()
        while time.time() - start < self._max_seconds:
            action = self._select(context)
            result = self._simulate(context.apply(action))
            self._back_prop(action, result)

        return self.best_action(root)

    def _select(self, context):
        return self, context

    def _simulate(self, context):
        return self, context

    def _back_prop(self, action, result):
        pass
