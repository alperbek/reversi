import time


def simple_match(env):
    """ A simple implementation of turn-based game match
    """
    print_game_start()

    turn = 1
    while env.is_active:
        start = print_turn_start(turn, env)
        action = env.agent.decide(env)
        env = env.apply(action)
        print_turn_end(start, action)
        turn += 1

    print_game_end(env)


def print_game_start():
    print_message("Game start")


def print_turn_start(turn, env):
    start = time.time()
    agent = env.agent
    print('[{}] Turn: {} ({})'.format(
        time.strftime("%H:%M:%S", time.localtime(start)), turn, agent))
    env.print_summary()
    return start


def print_turn_end(start, action):
    elapsed = time.time() - start
    print('Move: {} Elapsed: {:.2f}s\n'.format(action, elapsed))


def print_game_end(env):
    env.print_summary()
    print_message("Game end")


def print_message(message, width=40):
    print
    print('-' * width)
    print(message)
    print('-' * width)
    print


