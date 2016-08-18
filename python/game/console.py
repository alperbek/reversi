from agent.dummy import RandomAgent
from agent.manual import ManualAgent
from agent.minimax import MinimaxAgent, MinimaxABAgent
from agent.mcts import MCTSAgent


def choose_agent(message):
    while True:
        print
        print(message)
        print_horizontal_line()
        print('[1] Manual (Human)')
        print('[2] Random (Dummy)')
        print('[3] MiniMax (Naive)')
        print('[4] MiniMax (Alpha Beta Pruning)')
        print('[5] Monte Carlo Tree Search')
        # print('[6] Deep Q Learning Player')
        print_horizontal_line()
        try:
            number = eval(raw_input('Enter [1-6]: '))
            if number == 1:
                return ManualAgent()
            if number == 2:
                return RandomAgent()
            if number == 3:
                number = eval(raw_input('Max Depth: '))
                return MinimaxAgent(number)
            if number == 4:
                number = eval(raw_input('Max Depth: '))
                return MinimaxABAgent(number)
            if number == 5:
                number = eval(raw_input('Max Seconds: '))
                return MCTSAgent(number)
            if number == 6:
                raise NotImplementedError("Deep Q Learning Agent Not Implemented")
        except Exception as e:
            print(e)


def print_horizontal_line(width=40):
    print('-' * width)


