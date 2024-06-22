# Solution
import numpy as np


def cross_entropy_error(y, t):
    y = np.array(y)
    t = np.array(t)
    N = y.shape[0]
    # 誤差の計算
    loss = - 1/N * np.sum(t * np.log(y))
    return loss


N = int(input())
y = [list(map(float, input().split(' '))) for _ in range(N)]
t = [list(map(int, input().split(' '))) for _ in range(N)]

loss = cross_entropy_error(y, t)
print(loss)
