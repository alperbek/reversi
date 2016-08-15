import random

INFINITY = float('Inf')


class Player(object):
    def decide(self, context):
        return None

    def update(self, state, action, reward, new_state):
        pass


class RandomPlayer(Player):
    def decide(self, context):
        return random.choice(context.get_valid_actions(self))


class MiniMaxPlayer(Player):
    def __init__(self, max_depth):
        self._max_depth = max_depth
        self._opponent = None

    def decide(self, context):
        self._opponent = context.get_opponent(self)
        actions = context.get_valid_actions(self)
        scores = map(lambda action: self._min_play(context.apply(self, action), 1), actions)
        return actions[scores.index(max(scores))]

    def _min_play(self, context, depth):
        if not context.is_active() or depth > self._max_depth:
            return context.get_score(self)
        actions = context.get_valid_actions(self._opponent)
        if len(actions) == 0:
            return self._max_play(context, depth)
        return min(map(lambda action: self._max_play(context.apply(self._opponent, action), depth+1), actions))

    def _max_play(self, context, depth):
        if not context.is_active() or depth > self._max_depth:
            return context.get_score(self)
        actions = context.get_valid_actions(self)
        if len(actions) == 0:
            return self._min_play(context, depth)
        return max(map(lambda action: self._min_play(context.apply(self, action), depth+1), actions))
