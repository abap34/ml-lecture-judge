# Solution
import numpy as np

# take input
n = int(input())
y = list(map(float, input().split()))
x = list(map(float, input().split()))

# convert to numpy array
y = np.array(y)
x = np.array(x)

import matplotlib.pyplot as plt
plt.plot(x, y, 'o')
plt.savefig("test.png") 

# compute lse
yb = np.mean(y)
xb = np.mean(x)

beta = np.dot(y - yb, x - xb) / np.dot(x - xb, x - xb)
alpha = yb - beta*xb

# compute mse
mse = np.mean((y - alpha - beta*x)**2)

# print answer
print(mse)