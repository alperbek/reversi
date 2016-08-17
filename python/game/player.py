import random
#import time

INFINITY = float('Inf')


class Player(object):
    def decide(self, context):
        """ Returns an action to take (or None to skip)
        """
        return None

    def __str__(self):
        return self.__class__.__name__


class RandomPlayer(Player):
    def decide(self, context):
        actions = context.get_valid_actions()
        if len(actions) == 0:
            return None
        return random.choice(actions)


class ManualPlayer(Player):
    def decide(self, context):
        valid_actions = context.get_valid_actions()
        if len(valid_actions) == 0:
            return None
        while True:
            command = raw_input('Enter a move row, col: ')
            if command == 'quit':
                exit(0)
            elif command == 'show':
                print('Valid moves: {}'.format(valid_actions))
            elif command == 'help':
                print('quit: terminate the match')
                print('help: show this help')
            else:
                try:
                    action = eval(command)
                except Exception as e:
                    print('Invalid input: {}'.format(e))
                if action in valid_actions:
                    return action
                print('Invalid move: {}'.format(action))


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


class MinimaxPlayer(Player):
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
        return arg_max(context.get_valid_actions(),
                       lambda action: self._min_play(context.apply(action), 1))

    def _max_play(self, context, depth):
        if not context.is_active() or depth > self._max_depth:
            return context.get_score()
        return val_max(context.get_valid_actions(),
                       lambda action: self._min_play(context.apply(action), depth+1))

    def _min_play(self, context, depth):
        if not context.is_active() or depth > self._max_depth:
            return context.get_score()
        return val_min(context.get_valid_actions(),
                       lambda action: self._max_play(context.apply(action), depth+1))


class MinimaxAlphaBetaPlayer(Player):
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
        return arg_max(context.get_valid_actions(),
                       lambda action: self._min_play(context.apply(action),
                                                     -INFINITY, INFINITY, 1))

    def _max_play(self, context, alpha, beta, depth):
        if not context.is_active() or depth > self._max_depth:
            return context.get_score()
        actions = context.get_valid_actions()
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
        if not context.is_active() or depth > self._max_depth:
            return context.get_score()
        actions = context.get_valid_actions()
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


# TODO work in progress
# class MonteCarloTreeSearchPlayer(Player):
#    def __init__(self, max_seconds):
#        self._max_seconds = max_seconds
#
#    def decide(self, context):
#        start = time.time()
#        while time.time() - start < self._max_seconds:
#            action = self._select(context)
#            result = self._simulate(context.apply(action))
#            self._back_prop(action, result)
#
#        return self.best_action(root)
#
#    def _select(self, context):
#        return self, context
#
#    def _simulate(self, context):
#        return self, context
#
#    def _back_prop(self, action, result):
#        pass


def print_horizontal_line(width=40):
    print('-' * width)


def choose_player(message):
    while True:
        print_horizontal_line()
        print(message)
        print_horizontal_line()
        print('[0] Manual (Human) Player')
        print('[1] Random Player')
        print('[2] MiniMax (Naive) Player')
        print('[3] MiniMax (Alpha Beta Pruning) Player')
        # print('[4] Monte Carlo Tree Search Player')
        # print('[5] Deep Q Learning Player')
        print_horizontal_line()
        try:
            number = eval(raw_input('Enter [0-5]: '))
            print
            if number == 0:
                return ManualPlayer()
            if number == 1:
                return RandomPlayer()
            if number == 2:
                number = eval(raw_input('Max Depth: '))
                return MinimaxPlayer(number)
            if number == 3:
                number = eval(raw_input('Max Depth: '))
                return MinimaxAlphaBetaPlayer(number)
            # if number == 4:
            #    number = eval(raw_input('Max Seconds: '))
            #    return MonteCarloTreeSearchPlayer(number)
            # if number == 5:
            #    raise NotImplementedError("Deep Q Learning Player Not Implemented")
        except Exception as e:
            print(e)
