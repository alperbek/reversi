class Agent(object):
    def decide(self, env):
        """ Returns an action to take (or None to skip)
        """
        return None

    def __str__(self):
        return self.__class__.__name__
