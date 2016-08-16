import time


def simple_match(context):
    """ A simple implementation of turn-based game match
    """
    print_message("Game start")

    turn = 1
    while context.is_active():
        player = context.get_player()
        start = print_turn_start(turn, context)
        action = player.decide(context)
        context = context.apply(action)
        print_turn_end(start, action)
        turn += 1

    print_message("Game end")


def print_message(message, width=40):
    print('-' * width)
    print(message)
    print('-' * width)
    print


def print_turn_start(turn, context):
    start = time.time()
    player = context.get_player()
    print('[{}] Turn: {} ({})'.format(time.strftime("%H:%M:%S", time.localtime(start)), turn, player))
    context.print_summary()
    return start


def print_turn_end(start, action):
    elapsed = time.time() - start
    print('Move: {} Elapsed: {:.2f}s\n'.format(action, elapsed))
