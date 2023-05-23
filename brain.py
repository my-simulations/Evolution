import numpy as np


def leaky_relu(x: np.ndarray):
    pos_x = np.where(x>=0, x, 0)
    neg_x = np.where(x<0, x, 0)
    return pos_x + 0.01*neg_x


def func(x: np.ndarray):
    '''
    x - np.ndarray with shape=(6,) or shape=(5,)
    return tuple(np.ndarray(p1, p2, p3, p4, p5, p6), int) or tuple(np.ndarray(p1, p2, p3, p4, p5), int)
    where p1, p2, p3 - probabilities for idx_to_move,
    p4 - prabability for rotate, p5 - probability for reproduction,
    p6 - probability for photosynthesis only for herbivores
    and int - direction for rotating
    '''
    p = x[:-1]
    p = np.exp(p) / np.sum(np.exp(p))
    y = int(np.abs(x[-1]))
    return p, y


class linear:

    def __init__(self, input_dim: int, output_dim: int, weights: np.ndarray=None):
        if weights:
            if weights.shape != (input_dim, output_dim):
                raise AttributeError('Wrong weights')
            
            self.weights = weights
        else:
            self.weights = self.init_weights(input_dim, output_dim)
    
    def init_weights(self, input_dim, output_dim):
        return np.random.uniform(-2, 2, size=(input_dim, output_dim))

    def forward(self, data: np.ndarray):
        '''
        data - np.ndarray with shape=(input_dim,)
        '''
        return data @ self.weights


class network:

    def __init__(self, type: int, weights1: np.ndarray=None, weights2: np.ndarray=None):
        '''
        type=2 for herbivores
        type=3 for predators
        '''
        if weights1:
            self.linear1 = linear(input_dim=14, output_dim=11, weights=weights1)
        else:
            self.linear1 = linear(input_dim=14, output_dim=11)

        if weights2:
            if type == 2:
                self.linear2 = linear(input_dim=11, output_dim=7, weights=weights2)
            elif type == 3:
                self.linear2 = linear(input_dim=11, output_dim=6, weights=weights2)
            else:
                raise AttributeError('Incorrect type')
        else:
            if type == 2:
                self.linear2 = linear(input_dim=11, output_dim=7)
            elif type == 3:
                self.linear2 = linear(input_dim=11, output_dim=6)
            else:
                raise AttributeError('Incorrct type')
    
    def forward(self, data0: np.ndarray):
        '''
        data0 - np.ndarray with shape=(14,)
        return data2 - tuple (np.ndarray(5,), int) for herbivores
        return data2 - tuple (np.ndarray(4,), int) for predators
        '''
        data1 = leaky_relu(self.linear1.forward(data0))
        data2 = func(self.linear2.forward(data1))
        return data2