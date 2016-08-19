class State(object):
    def __init__(self, board, agent, opponent, agent_score, opponent_score):
        self.board = board
        self.agent = agent
        self.opponent = opponent
        self.agent_score = agent_score
        self.opponent_score = opponent_score

    def turn(self, board, reward, opponent_reward):
        return State(board,
                     self.opponent,
                     self.agent,
                     self.opponent_score + opponent_reward,
                     self.agent_score + reward)

    def opposite(self):
        return self.turn(self.board, 0, 0)

    def score(self, agent):
        if self.agent == agent:
            return self.agent_score
        else:
            return self.opponent_score

    def __eq__(self, other):
        return self.board == other.board and self.agent == other.agent

    def __hash__(self):
        return hash(self.board)
