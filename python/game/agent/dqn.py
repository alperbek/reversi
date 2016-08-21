from agent import Agent
import random
import numpy as np
import collections
import tensorflow as tf

dqn_file_name = 'DQN-learn'


class DQN(object):
    def __init__(self, rows, cols, learning_rate=0.001):
        size = rows * cols
        self._x = x = tf.placeholder(tf.float32, [None, size])
        self._y = y = tf.placeholder(tf.float32, [None, size])
        w = tf.Variable(tf.truncated_normal([size, size]))
        b = tf.Variable(tf.truncated_normal([size]))
        self._prediction = tf.nn.softmax(tf.matmul(x, w)+b)
        cross_entropy = y * tf.log(self._prediction)
        cost = tf.reduce_mean(-tf.reduce_sum(cross_entropy, 1))
        self._optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
        self._saver = tf.train.Saver([w, b])
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self._sess = tf.Session(config=config)
        self._sess.run(tf.initialize_all_variables())

    def end(self):
        self._sess.close()

    def train(self, x, y):
        self._sess.run(self._optimizer, feed_dict={self._x: x, self._y: y})

    def predict(self, x):
        return self._sess.run(self._prediction, feed_dict={self._x: x})

    def save(self):
        self._saver.save(self._sess, dqn_file_name)

    def restore(self):
        self._saver.restore(self._sess, dqn_file_name)


class DQNAgent(Agent):
    """ Deep Q Network Agent

    It uses the Q-learning with Deep Learning as Q-function approximation.
    """
    def __init__(self, (rows, cols),
                 learning_on=True,
                 gamma=0.9,
                 buffer_size=20,
                 batch_size=10):
        self._dqn = DQN(rows, cols)
        self._learning_on = learning_on
        self._gamma = gamma
        self._replay = collections.deque([], buffer_size)
        self._batch_size = min(batch_size, buffer_size)

    def start(self):
        self._dqn.restore()

    def end(self):
        self._dqn.save()
        self._dqn.end()

    def decide(self, env, state):
        valid_actions = env.valid_actions(state)
        if len(valid_actions) == 0:
            return None

        # evaluate the current state
        action = self._choose(state, valid_actions)

        # learn from the experience (including the opponent action which is reflected in this agent's score)
        self._learn(state, action, valid_actions)

        return action

    def _learn(self, state, action, valid_actions):
        if not self._learning_on:
            return
        s = state.board.data
        a = action[0] * state.board.cols + action[1]
        sc = state.score(self)
        va = [a[0] * state.board.cols + a[1] for a in valid_actions]
        if len(self._replay) == 0:
            self._replay.append((s, a, sc, va))
        elif len(self._replay) == 1:
            self._replay[0] = self._replay[0] + (s, a, sc, va)
        else:
            self._replay.append(self._replay[-1][4:] + (s, a, sc, va))
        if len(self._replay) >= self._batch_size:
            x, y = [], []
            for s1, a1, sc1, va1, s2, a2, sc2, va2 in random.sample(self._replay, self._batch_size):
                x.append(s1)
                p = self._predict(s1)
                p[a1] = (sc2 - sc1) + self._gamma * max(self._predict(s2))
                y.append([p[i] if i in va else 0.0 for i in range(len(p))])
            self._train(x, y)

    def _choose(self, state, valid_actions):
        # Boltzmann distribution
        p = self._predict(state.board.data)
        i = np.argmax(p)
        if random.random() < np.exp(p[i])/sum(np.exp(p)):
            action = i // state.board.rows, i // state.board.cols
            if action in valid_actions:
                return action
        return random.choice(valid_actions)

    def _predict(self, state):
        return self._dqn.predict([state])[0]

    def _train(self, x, y):
        return self._dqn.train(x, y)
