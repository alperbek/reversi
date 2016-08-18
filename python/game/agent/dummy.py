from agent import Agent
import random


class RandomAgent(Agent):
    def decide(self, env):
        actions = env.valid_actions
        if len(actions) == 0:
            return None
        return random.choice(actions)
