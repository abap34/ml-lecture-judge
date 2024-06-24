# Solution
import numpy as np

a, b = map(int, input().split())
x = np.array(list(map(int, input().split())))
y = np.array(list(map(int, input().split())))


def se(y, pred):
    return np.sum((y - pred) ** 2)


print(se(y, a * x + b))
