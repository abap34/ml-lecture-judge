# Solution
import numpy as np

n = int(input())
x = np.array(list(map(float, input().split())))
y = np.array(list(map(float, input().split())))

a = np.sum(x * y) / np.sum(x * x)

L_hat_a = np.mean((y - a * x)**2)

print(L_hat_a)

