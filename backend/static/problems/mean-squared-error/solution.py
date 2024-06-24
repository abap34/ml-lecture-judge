# Solution
import numpy as np

a, b = map(int, input().split())
x = np.array(list(map(int, input().split())))
y = np.array(list(map(int, input().split())))


def mse(y, pred):
    return np.mean((y - pred) ** 2)


print(mse(y, a * x + b))
