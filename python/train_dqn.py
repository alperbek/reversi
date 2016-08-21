from game.framework.match import SimpleMatch
from game.framework.state import State
from game.agent.dqn import DQNAgent
from game.console import choose_agent
from reversi import Reversi, create_board, Disc
import time


if __name__ == '__main__':
    board_size = (8, 8)
    black = choose_agent('Choose a black agent', board_size, Disc.BLACK.value)
    white = DQNAgent(board_size, Disc.WHITE.value)
    match = SimpleMatch(Reversi(black, white), logging_on=False)
    for i in range(10000):
        winner = match.run(State(create_board(board_size), black, white, 2, 2))
        print('[{}] #{} Winner: {}'.format(
            time.strftime("%H:%M:%S", time.localtime(time.time())), i, winner))
