import time


def simple_match(context):
    """ A simple implementation of turn-based game match
    """
    print_game_start()

    turn = 1
    while context.is_active:
        start = print_turn_start(turn, context)
        action = context.agent.decide(context)
        context = context.apply(action)
        print_turn_end(start, action)
        turn += 1

    print_game_end(context)


def print_game_start():
    print_message("Game start")


def print_turn_start(turn, context):
    start = time.time()
    agent = context.agent
    print('[{}] Turn: {} ({})'.format(
        time.strftime("%H:%M:%S", time.localtime(start)), turn, agent))
    context.print_summary()
    return start


def print_turn_end(start, action):
    elapsed = time.time() - start
    print('Move: {} Elapsed: {:.2f}s\n'.format(action, elapsed))


def print_game_end(context):
    context.print_summary()
    print_message("Game end")


def print_message(message, width=40):
    print
    print('-' * width)
    print(message)
    print('-' * width)
    print


