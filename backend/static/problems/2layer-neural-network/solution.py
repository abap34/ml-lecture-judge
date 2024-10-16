# Solution
import numpy as np

# 入力の受け取り
n, m, k = map(int, input().split())
x = np.array(list(map(int, input().split())))
w1 = np.array([list(map(int, input().split())) for _ in range(m)])
b1 = np.array(list(map(int, input().split())))
w2 = np.array([list(map(int, input().split())) for _ in range(k)])
b2 = np.array(list(map(int, input().split())))

u1 = np.dot(w1, x) + b1
z1 = np.maximum(u1, 0)
y = np.dot(w2, z1) + b2
print(*y)
