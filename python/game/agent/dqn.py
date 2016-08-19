from agent import Agent
import random


class DQNAgent(Agent):
    """ Deep Q Network Agent

    It uses the Q-learning with Deep Learning as Q-function approximation.
    """
    def decide(self, env, state):
        actions = env.valid_actions(state)
        if len(actions) == 0:
            return None
        return random.choice(actions)
