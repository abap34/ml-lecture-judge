# Solution
import numpy as np

x = eval(input())


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x))


print(softmax(x))
