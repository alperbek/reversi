import time


def simple_match(context):
    """ A simple implementation of turn-based game match
    """
    print("Game start")
    context.summary()

    turn = 1
    while context.is_active():
        player = context.get_player()
        print_progress(turn, player)
        action = player.decide(context)
        context = context.apply(action)
        context.summary()
        turn += 1

    print("Game end")


def print_progress(turn, player):
    print('[{}] Turn: {} ({})'.format(
        time.strftime("%H:%M:%S", time.localtime()), turn, player))
