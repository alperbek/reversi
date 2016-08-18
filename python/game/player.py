class GamePlayer(object):
    def __init__(self, agent, kind, score):
        self._agent = agent
        self._kind = kind
        self._score = score

    @property
    def agent(self):
        return self._agent

    @property
    def kind(self):
        return self._kind

    @property
    def score(self):
        return self._score

    def apply(self, score_change):
        return GamePlayer(self.agent, self.kind, self.score + score_change)

    def __str__(self):
        return '{}: {} ({})'.format(self.kind, self.score, self.agent)

    def __eq__(self, other):
        return self.agent == other.agent

