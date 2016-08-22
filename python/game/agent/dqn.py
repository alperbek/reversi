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
        prediction = tf.nn.tanh(tf.matmul(h2, w3) + b3)
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
                 learning_rate=0.001,
                 alpha=0.1,
                 gamma=1.0,
                 epsilon=0.6):
        self._dqn = DQN(rows, cols, learning_rate)
        self._sign = sign
        self._learning_on = learning_on
        self._alpha = alpha
        self._gamma = gamma
        self._epsilon = epsilon
        self._costs = []
        self._prev_move = None

    def decide(self, env, state):
        valid_actions = env.valid_actions(state)
        if len(valid_actions) == 0:
            return None

        st = state.board.data(self._sign)
        qv = self._dqn.predict([st])[0]

        for action in [(row, col) for row in range(state.board.rows)
                       for col in range(state.board.cols)]:
            ai = action_index(state.board, action)
            if action in valid_actions:
                qv[ai] = max(qv[ai], -0.99)
            else:
                qv[ai] = -1.0

        ai = np.argmax(qv)
        action = index_action(state.board, ai)
        if self._learning_on:
            # exploration
            p = np.exp(qv[ai])/np.sum(np.exp(qv))
            if p < random.random() * self._epsilon:
                action = random.choice(valid_actions)
            # train q-func
            if self._prev_move is not None:
                ost, oai, oqv = self._prev_move
                oqv[oai] += self._alpha * (self._gamma * max(qv) - oqv[oai])
                self._costs.append(self._dqn.train([ost], [oqv]))
            self._prev_move = (st, ai, qv)

        return action

    def end(self, winner):
        if self._learning_on:
            reward = 0.0 if winner is None else 1.0 if winner == self else -1.0
            ost, oai, oqv = self._prev_move
            oqv[oai] += self._alpha * (reward - oqv[oai])
            self._costs.append(self._dqn.train([ost], [oqv]))
            print 'Epsilon: {:.3f} Cost: {:.2f}'.format(
                self._epsilon, sum(self._costs)/len(self._costs))
            self._costs = []
            self._epsilon = max(self._epsilon - 0.001, 0.0)
            self._prev_move = None
        self._dqn.end()
