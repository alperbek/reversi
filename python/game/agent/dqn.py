from agent import Agent
import random
import numpy as np
import tensorflow as tf
import os.path

dqn_file_name = 'DQN-learn'


class DQN(object):
    def __init__(self, rows, cols, learning_rate):
        size = rows * cols
        # features and labels
        x = tf.placeholder(tf.float32, [None, size])
        y = tf.placeholder(tf.float32, [None, size])
        # parameters
        w1 = tf.Variable(tf.truncated_normal([size, size]))
        b1 = tf.Variable(tf.truncated_normal([size]))
        w2 = tf.Variable(tf.truncated_normal([size, size]))
        b2 = tf.Variable(tf.truncated_normal([size]))
        w3 = tf.Variable(tf.truncated_normal([size, size]))
        b3 = tf.Variable(tf.truncated_normal([size]))
        # feed forward
        h1 = tf.nn.relu(tf.matmul(x, w1) + b1)
        h2 = tf.nn.relu(tf.matmul(h1, w2) + b2)
        prediction = tf.nn.softmax(tf.matmul(h2, w3) + b3)
        # optimization
        cost = tf.reduce_mean(tf.nn.l2_loss(prediction - y))
        optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)
        # for later use
        self._x = x
        self._y = y
        self._prediction = prediction
        self._optimizer = optimizer
        self._cost = cost
        self._saver = tf.train.Saver([w1, b1, w2, b2, w3, b3])
        # session
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self._sess = tf.Session(config=config)
        self._sess.run(tf.initialize_all_variables())
        # persistence
        if os.path.isfile(dqn_file_name):
            self._saver.restore(self._sess, dqn_file_name)

    def end(self):
        self._saver.save(self._sess, dqn_file_name)
        # self._sess.close()

    def train(self, x, y):
        _, cost = self._sess.run([self._optimizer, self._cost], feed_dict={self._x: x, self._y: y})
        return cost

    def predict(self, x):
        return self._sess.run(self._prediction, feed_dict={self._x: x})


def action_index(board, action):
    return action[0] * board.cols + action[1]


def index_action(board, ai):
    return int(ai / board.rows), int(ai % board.cols)


class DQNAgent(Agent):
    """ Deep Q Network Agent

    It uses the Q-learning with Deep Learning as Q-function approximation.
    """
    def __init__(self, (rows, cols),
                 sign,
                 learning_on=True,
                 learning_rate=0.0001,
                 gamma=0.8,
                 epsilon=0.99):
        self._dqn = DQN(rows, cols, learning_rate)
        self._sign = sign
        self._learning_on = learning_on
        self._gamma = gamma
        self._epsilon = epsilon
        self._replay = []

    def end(self, winner):
        self._train(winner)
        self._dqn.end()
        self._replay = []

    def decide(self, env, state):
        valid_actions = env.valid_actions(state)
        if len(valid_actions) == 0:
            return None

        # evaluate the current state
        action = self._choose(state, valid_actions)

        # learn from the experience (including the opponent action which is reflected in this agent's score)
        self._learn(state, action)

        return action

    def _choose(self, state, valid_actions):
        p = self._predict(state.board.data(self._sign))
        ai = np.argmax(p)
        if not self._learning_on or random.random() * self._epsilon <= p[ai]:
            action = index_action(state.board, ai)
            if action in valid_actions:
                return action
        return random.choice(valid_actions)

    def _predict(self, state):
        return self._dqn.predict([state])[0]

    def _learn(self, state, action):
        if not self._learning_on:
            return
        st = state.board.data(self._sign)
        ai = action_index(state.board, action)
        self._replay.append((st, ai))

    def _train(self, winner):
        if not self._learning_on:
            return
        reward = 0 if winner is None else 1 if winner == self else -1
        x, y = [], []
        last_index = len(self._replay)-1
        for i in range(last_index, 0, -1):
            st, ai = self._replay[i]
            qv = self._predict(st)
            qv[ai] = reward
            if i != last_index:
                st2, ai2 = self._replay[i+1]
                qv[ai] += self._gamma * max(self._predict(st2))
            x.append(st)
            y.append(qv)
        cost = self._dqn.train(x, y)
        print 'Training Cost: {:.2f}'.format(cost)
