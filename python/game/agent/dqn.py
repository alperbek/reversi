from agent import Agent
import random
import numpy as np
import tensorflow as tf
import os.path
from collections import deque

FILE_DQN_LEARNING_ON = 'dqn_learning_on'
FIlE_DQN_LEARNING_OFF = 'dqn_learning_off'


class DQN(object):
    def __init__(self, rows, cols, learning_rate, learning_on):
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
        self._learning_on = learning_on
        # session
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self._sess = tf.Session(config=config)
        self._sess.run(tf.initialize_all_variables())
        # persistence
        if learning_on:
            if os.path.isfile(FILE_DQN_LEARNING_ON):
                self._saver.restore(self._sess, FILE_DQN_LEARNING_ON)
            elif os.path.isfile(FIlE_DQN_LEARNING_OFF):
                self._saver.restore(self._sess, FIlE_DQN_LEARNING_OFF)

    def save(self):
        if self._learning_on:
            self._saver.save(self._sess, FILE_DQN_LEARNING_ON)

    def train(self, x, y):
        _, cost = self._sess.run([self._optimizer, self._cost], feed_dict={self._x: x, self._y: y})
        return cost

    def predict(self, x):
        return self._sess.run(self._prediction, feed_dict={self._x: x})


def action_to_index(board, action):
    return action[0] * board.cols + action[1]


def index_to_action(board, ai):
    return int(ai / board.rows), int(ai % board.cols)


class DQNAgent(Agent):
    """ Deep Q Network Agent

    It uses the Q-learning with Deep Learning as Q-function approximation.
    """
    def __init__(self, (rows, cols),
                 sign,
                 learning_on=True,
                 learning_rate=0.0001,
                 alpha=0.1,
                 gamma=1.0,
                 epsilon=0.6):
        self._dqn = DQN(rows, cols, learning_rate, learning_on)
        self._sign = sign
        self._learning_on = learning_on
        self._alpha = alpha
        self._gamma = gamma
        self._epsilon = epsilon
        self._costs = []
        self._replay = deque([], 1000)
        self._batch_size = 100

    def decide(self, env, state):
        valid_actions = env.valid_actions(state)
        if len(valid_actions) == 0:
            return None

        q_states = state.board.data(self._sign)
        q_values = self._dqn.predict([q_states])[0]

        rows, cols = state.board.rows, state.board.cols
        for action in [(row, col) for row in range(rows) for col in range(cols)]:
            action_index = action_to_index(state.board, action)
            if action in valid_actions:
                q_values[action_index] = min(max(q_values[action_index], -0.99), 1.0)
            else:
                q_values[action_index] = -1.0

        # greedy
        chosen_action_index = np.argmax(q_values)

        if self._learning_on:
            # train q-func
            if len(self._replay) > self._batch_size*2:
                self._train(reward=0)

            # exploration by epsilon
            p = np.exp(q_values[chosen_action_index])/np.sum(np.exp(q_values))
            if min(p, random.random()) < self._epsilon:
                action = random.choice(valid_actions)
                chosen_action_index = action_to_index(state.board, action)

            # append the new states and values for the next training
            q_values[chosen_action_index] = self._alpha * (self._gamma * max(q_values) - q_values[chosen_action_index])
            move = [q_states, chosen_action_index, q_values]
            self._replay.append(move)

        return index_to_action(state.board, chosen_action_index)

    def _train(self, reward):
        # update the last move with reward
        q_states, chosen_action_index, q_values = self._replay[-1]
        q_values[chosen_action_index] += self._alpha * reward
        self._replay[-1][-1] = q_values
        # experience replay with the last move
        replay_indices = np.random.randint(0, len(self._replay)-1, self._batch_size)
        random_position = np.random.randint(0, self._batch_size)
        replay_indices[random_position] = -1
        # train q-network
        experience_replay = [self._replay[index] for index in replay_indices]
        x, y = zip(*[(q_states, q_values) for q_states, _, q_values in experience_replay])
        self._costs.append(self._dqn.train(x, y))

    def end(self, winner):
        if self._learning_on:
            self._train(reward=0.0 if winner is None else 1.0 if winner == self else -1.0)
            print 'Epsilon: {:.3f} Cost: {:.2f}'.format(self._epsilon, sum(self._costs)/len(self._costs))
            self._costs = []
            self._epsilon = max(self._epsilon - 0.001, 0.0)
            self._dqn.save()


