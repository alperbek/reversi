from agent import Agent
import random


class RandomAgent(Agent):
    def decide(self, context):
        actions = context.valid_actions
        if len(actions) == 0:
            return None
        return random.choice(actions)
