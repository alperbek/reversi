from players.dummy import RandomPlayer
from players.manual import ManualPlayer
from players.minimax import MinimaxPlayer, MinimaxAlphaBetaPlayer
from players.mcts import MonteCarloTreeSearchPlayer


def choose_player(message):
    while True:
        print
        print(message)
        print_horizontal_line()
        print('[1] Manual (Human) Player')
        print('[2] Random Player')
        print('[3] MiniMax (Naive) Player')
        print('[4] MiniMax (Alpha Beta Pruning) Player')
        print('[5] Monte Carlo Tree Search Player')
        # print('[6] Deep Q Learning Player')
        print_horizontal_line()
        try:
            number = eval(raw_input('Enter [1-6]: '))
            if number == 1:
                return ManualPlayer()
            if number == 2:
                return RandomPlayer()
            if number == 3:
                number = eval(raw_input('Max Depth: '))
                return MinimaxPlayer(number)
            if number == 4:
                number = eval(raw_input('Max Depth: '))
                return MinimaxAlphaBetaPlayer(number)
            if number == 5:
                number = eval(raw_input('Max Seconds: '))
                return MonteCarloTreeSearchPlayer(number)
            if number == 6:
                raise NotImplementedError("Deep Q Learning Player Not Implemented")
        except Exception as e:
            print(e)


def print_horizontal_line(width=40):
    print('-' * width)


