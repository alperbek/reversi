from agent import Agent

INFINITY = float('Inf')


def val_max(seq, fn):
    if len(seq) == 0:
        return fn(None)
    return max(map(fn, seq))


def val_min(seq, fn):
    if len(seq) == 0:
        return fn(None)
    return min(map(fn, seq))


def arg_max(seq, fn):
    if len(seq) == 0:
        return None
    values = map(fn, seq)
    return seq[values.index(max(values))]


class MinimaxAgent(Agent):
    """ Naive minimax player

    Minimax player iterate though all the valid moves to find the best (highest value) move.
    For each, it needs to evaluate all the possible following moves by the opponent
    who tries to choose the best move which is the worst move for this player.
    This traversing of possible move chains will be continued until we reach the max depth
    or there is no more move for both players.
    """
    def __init__(self, max_depth):
        self._max_depth = max_depth

    def decide(self, context):
        return arg_max(context.valid_actions,
                       lambda action: self._min_play(context.apply(action), 1))

    def _max_play(self, context, depth):
        if not context.is_active or depth > self._max_depth:
            return context.score
        return val_max(context.valid_actions,
                       lambda action: self._min_play(context.apply(action), depth+1))

    def _min_play(self, context, depth):
        if not context.is_active or depth > self._max_depth:
            return context.score
        return val_min(context.valid_actions,
                       lambda action: self._max_play(context.apply(action), depth+1))


class MinimaxABAgent(Agent):
    """ An improved version of minimax player.

    The player (=max player) will choose the best of the worst moves chosen by the
    min player, and the opponent (=min player) will choose the worst of the best
    moves chosen by the max player.

    The max player can stop traversing child nodes if the current node value is already
    bigger than other sibling nodes (that were evaluated before that node) as the min
    player will not choose the node anyway.

    The min player can stop traversing child nodes if the current node value is already
    smaller than other sibling nodes (that were evaluated before that node) as the max
    player will not choose the node anyway.

    Alpha is the best of the worst values chosen by the min player from the child nodes.
    If the min player finds that the current node value is less than the alpha, it stops.

    Beta is the worst of the best values chosen by the max player from the child nodes.
    If the max player finds that the current node value is more than the beta, it stops.
    """
    def __init__(self, max_depth):
        self._max_depth = max_depth

    def decide(self, context):
        return arg_max(context.valid_actions,
                       lambda action: self._min_play(context.apply(action),
                                                     -INFINITY, INFINITY, 1))

    def _max_play(self, context, alpha, beta, depth):
        if not context.is_active or depth > self._max_depth:
            return context.score
        actions = context.valid_actions
        if len(actions) == 0:
            return self._min_play(context.apply(None),
                                  alpha, beta, depth)
        value = -INFINITY
        for action in actions:
            value = max(value, self._min_play(context.apply(action),
                                              alpha, beta, depth+1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def _min_play(self, context, alpha, beta, depth):
        if not context.is_active or depth > self._max_depth:
            return context.score
        actions = context.valid_actions
        if len(actions) == 0:
            return self._max_play(context.apply(None),
                                  alpha, beta, depth)
        value = INFINITY
        for action in actions:
            value = min(value, self._max_play(context.apply(action),
                                              alpha, beta, depth+1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value
