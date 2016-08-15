import os


def simple_match(context):
    """ A simple implementation of turn-based game match

    :param context: a game context providing implementation of game.context.GameContext interface
    :return: None
    """
    turn = 1
    # run while the game is active
    while context.is_active():
        if len(context.get_valid_actions()) > 0:
            player = context.get_player()
            action = player.decide(context)
            # context is immutable - apply will return a new instance
            state = context.get_state()
            score = context.get_score(player)
            context = context.apply(action)
            if action is not None:
                reward = context.get_score(player) - score
                new_state = context.get_state()
                player.update(state, action, reward, new_state)
                print(os.linesep + str(new_state))
                print('Turn: {} {}'.format(turn, context.summary()))
                turn += 1
