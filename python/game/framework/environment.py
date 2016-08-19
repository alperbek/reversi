class Environment(object):
    def is_active(self, state):
        return False

    def valid_actions(self, state):
        return []

    def apply(self, state, action):
        return None

    def winner(self, state):
        return None

    def print_summary(self, state):
        pass
