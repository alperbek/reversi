import random

INFINITY = float('Inf')


def random_player(context):
    actions = context.get_valid_actions()
    if len(actions) == 0:
        return None
    return random.choice(actions)


def manual_player(context):
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


def minimax_player(root_context, max_depth):
    def max_player(context, depth):
        if not context.is_active() or depth > max_depth:
            return context.get_score()
        return val_max(context.get_valid_actions(),
                       lambda action: min_player(context.apply(action), depth+1))

    def min_player(context, depth):
        if not context.is_active() or depth > max_depth:
            return context.get_score()
        return val_min(context.get_valid_actions(),
                       lambda action: max_player(context.apply(action), depth+1))

    return arg_max(root_context.get_valid_actions(),
                   lambda action: min_player(root_context.apply(action), 1))


def minimax_alpha_beta_player(root_context, max_depth):
    def max_player(context, alpha, beta, depth):
        if not context.is_active() or depth > max_depth:
            return context.get_score()
        actions = context.get_valid_actions()
        if len(actions) == 0:
            return min_player(context.apply(None), alpha, beta, depth)
        value = -INFINITY
        for action in actions:
            value = max(value, min_player(context.apply(action), alpha, beta, depth+1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_player(context, alpha, beta, depth):
        if not context.is_active() or depth > max_depth:
            return context.get_score()
        actions = context.get_valid_actions()
        if len(actions) == 0:
            return max_player(context.apply(None), alpha, beta, depth)
        value = INFINITY
        for action in actions:
            value = min(value, max_player(context.apply(action), alpha, beta, depth+1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    return arg_max(root_context.get_valid_actions(),
                   lambda action: min_player(root_context.apply(action), -INFINITY, INFINITY, 1))


def choose_player(message):
    while True:
        print(message)
        print('[1] Random Player')
        print('[2] MiniMax (Naive) Player')
        print('[3] MiniMax (Alpha Beta Pruning) Player')
        print('[4] Manual (Human) Player')
        try:
            number = eval(raw_input('Enter [1-4]: '))
            if number == 1:
                return random_player
            if number == 2:
                number = eval(raw_input('Max Depth: '))
                return lambda context: minimax_player(context, number)
            if number == 3:
                number = eval(raw_input('Max Depth: '))
                return lambda context: minimax_alpha_beta_player(context, number)
            if number == 4:
                return manual_player
        except Exception as e:
            print(e)
