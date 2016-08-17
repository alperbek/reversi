from player import Player
import time
import random
from math import log, sqrt


class StateInfo(object):
    def __init__(self):
        self.wins = 0
        self.plays = 0


class StateInfoMap(object):
    def __init__(self):
        self._states = {}
        self._c = sqrt(2.0)  # theoretically sqrt(2); in practice usually chosen empirically

    def add(self, state):
        if state not in self._states:
            self._states[state] = StateInfo()

    def exists(self, state):
        return state in self._states

    def has_explored(self, states):
        return all(self.exists(state) for state in states)

    def update_all(self, states, won):
        for state in states:
            self.update(state, won)

    def update(self, state, won):
        if not self.exists(state):
            return
        info = self._states[state]
        info.plays += 1
        if won:
            info.wins += 1

    def get_wins(self, state):
        if not self.exists(state):
            return 0
        return self._states[state].wins

    def get_plays(self, state):
        if not self.exists(state):
            return 0
        return self._states[state].plays

    def get_win_ratio(self, state):
        if not self.exists(state):
            return 0.0
        info = self._states[state]
        if info.plays == 0:
            return 0.0
        return info.wins * 1.0 / info.plays

    def get_best_state(self, states):
        """ Using UCB1 select the best state
        """
        log_sum = log(sum(self.get_plays(state) for state in states))
        _, best_state = max([(self.get_win_ratio(state)
                              + self._c * sqrt(log_sum / self.get_plays(state)), state)
                             for state in states])
        return best_state

    def get_best_action(self, context, actions):
        state_action_pairs = [(context.apply(action).get_state(), action) for action in actions]
        win_ratio, state, action = max((self.get_win_ratio(state), state, action)
                                       for state, action in state_action_pairs)
        wins, plays = self.get_wins(state), self.get_plays(state)
        return action, win_ratio, wins, plays


class MonteCarloTreeSearchPlayer(Player):
    def __init__(self, max_seconds):
        self._max_seconds = max_seconds
        self._state_info_map = StateInfoMap()

    def decide(self, context):
        valid_actions = context.get_valid_actions()
        if len(valid_actions) == 0:
            return None
        if len(valid_actions) == 1:
            return valid_actions[0]

        start = time.time()
        while time.time() - start < self._max_seconds:
            self._simulate(context)

        action, win_ratio, wins, plays = self._state_info_map.get_best_action(context, valid_actions)
        print('Win Ratio: {:.2f}% ({}/{})'.format(win_ratio * 100.0, wins, plays))
        return action

    def _simulate(self, context):
        expand = True
        visited = set()

        while context.is_active():
            # selection of action (aka context)
            contexts = [context.apply(action) for action in context.get_valid_actions()]
            if len(contexts) > 0:
                states = [context.get_state() for context in contexts]
                if self._state_info_map.has_explored(states):
                    # exploitation
                    context = self._state_info_map.get_best_state(states).get_context()
                else:
                    # exploration
                    context = random.choice(contexts)
            else:
                context = context.apply(None)  # pass to the opponent

            # expansion of tree / node
            state = context.get_state()
            visited.add(state)
            if expand:
                if not self._state_info_map.exists(state):
                    expand = False
                    self._state_info_map.add(state)

        # back propagation of wins / plays
        self._state_info_map.update_all(visited, context.get_winner() == self)
