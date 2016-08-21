import time


def simple_match(env, state):
    """ A simple implementation of turn-based game match
    """
    on_game_start(state)

    turn = 1
    while env.is_active(state):
        start = on_turn_start(turn, env, state)
        action = state.agent.decide(env, state)
        state = env.apply(state, action)
        on_turn_end(start, action)
        turn += 1

    on_game_end(env, state)


def on_game_start(state):
    print_message("Game start")
    state.agent.start()
    state.opponent.start()


def on_turn_start(turn, env, state):
    start = time.time()
    agent = state.agent
    print('[{}] Turn: {} ({})'.format(
        time.strftime("%H:%M:%S", time.localtime(start)), turn, agent))
    print(state.board)
    env.print_summary(state)
    return start


def on_turn_end(start, action):
    elapsed = time.time() - start
    print('Move: {} Elapsed: {:.2f}s\n'.format(action, elapsed))


def on_game_end(env, state):
    print('[{}] Winner: {}'.format(
        time.strftime("%H:%M:%S", time.localtime(time.time())), env.winner(state)))
    print(state.board)
    state.agent.end()
    state.opponent.end()
    env.print_summary(state)
    print_message("Game end")


def print_message(message, width=40):
    print
    print('-' * width)
    print(message)
    print('-' * width)
    print


