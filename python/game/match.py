def simple_match(context):
    """ A simple implementation of turn-based game match
    """
    print("Game start")
    turn = 1
    # run while the game is active
    while context.is_active():
        player = context.get_player()
        action = player(context)
        context = context.apply(action)
        print('Turn: {}'.format(turn))
        context.summary()
        turn += 1
    print("Game end")
