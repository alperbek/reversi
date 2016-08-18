class GamePlayer(object):
    def __init__(self, agent, kind, score):
        self._agent = agent
        self._kind = kind
        self._score = score

    def get_agent(self):
        return self._agent

    def get_kind(self):
        return self._kind

    def get_score(self):
        return self._score

    def apply(self, score_change):
        return GamePlayer(self._agent, self._kind, self._score + score_change)

    def __str__(self):
        return '{}: {} ({})'.format(self._kind, self._score, self._agent)

    def __eq__(self, other):
        return self.get_agent() == other.get_agent()

