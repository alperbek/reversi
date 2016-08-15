import random

INFINITY = float('Inf')


class Player(object):
    def decide(self, context):
        return None

    def update(self, state, action, reward, new_state):
        pass


class RandomPlayer(Player):
    def decide(self, context):
        return random.choice(context.get_valid_actions())


class ManualPlayer(Player):
    """ aka Human Player
    """
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


class MiniMaxPlayer(Player):
    def __init__(self, max_depth):
        self._max_depth = max_depth

    def decide(self, context):
        actions = context.get_valid_actions()
        scores = map(lambda action: self._min_play(context.apply(action), 1), actions)
        return actions[scores.index(max(scores))]

    def _min_play(self, context, depth):
        if not context.is_active() or depth > self._max_depth:
            return context.get_score(self)
        actions = context.get_valid_actions()
        if len(actions) == 0:
            return self._max_play(context.apply(None), depth)
        return min(map(lambda action: self._max_play(context.apply(action), depth+1), actions))

    def _max_play(self, context, depth):
        if not context.is_active() or depth > self._max_depth:
            return context.get_score(self)
        actions = context.get_valid_actions()
        if len(actions) == 0:
            return self._min_play(context.apply(None), depth)
        return max(map(lambda action: self._min_play(context.apply(action), depth+1), actions))


class MiniMaxAlphaBetaPruningPlayer(Player):
    def __init__(self, max_depth):
        self._max_depth = max_depth

    def decide(self, context):
        actions = context.get_valid_actions()
        scores = map(lambda action: self._min_play(context.apply(action), -INFINITY, INFINITY, 1), actions)
        return actions[scores.index(max(scores))]

    def _min_play(self, context, alpha, beta, depth):
        if not context.is_active() or depth > self._max_depth:
            return context.get_score(self)
        actions = context.get_valid_actions()
        if len(actions) == 0:
            return self._max_play(context.apply(None), alpha, beta, depth)
        value = INFINITY
        for action in actions:
            value = min(value, self._max_play(context.apply(action), alpha, beta, depth+1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def _max_play(self, context, alpha, beta, depth):
        if not context.is_active() or depth > self._max_depth:
            return context.get_score(self)
        actions = context.get_valid_actions()
        if len(actions) == 0:
            return self._min_play(context.apply(None), alpha, beta, depth)
        value = -INFINITY
        for action in actions:
            value = max(value, self._min_play(context.apply(action), alpha, beta, depth+1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value
