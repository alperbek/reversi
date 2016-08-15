def simple_match(context):
    """ A simple implementation of turn-based game match

    :param context: a game context providing implementation of game.context.GameContext interface
    :return: None
    """
    player = None
    turn = 1
    # run while the game is active
    while context.is_active():
        player = context.get_opponent(player)
        if len(context.get_valid_actions(player)) > 0:
            action = player.decide(context)
            if action is not None:
                # context is immutable - apply will return a new instance
                state = context.get_state()
                score = context.get_score(player)
                context = context.apply(player, action)
                reward = context.get_score(player) - score
                new_state = context.get_state()
                player.update(state, action, reward, new_state)
                print('\n{}'.format(new_state))
                print('Turn: {} {}'.format(turn, context.summary()))
            turn += 1
