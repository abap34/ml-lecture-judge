# 
# - $1 \leq n \leq 100$
# - $-1000 \leq y_i \leq 1000$
# - 入力は全て整数

import numpy as np

def gen():
    n = np.random.randint(1, 101)
    y = np.random.randint(-1000, 1001, n)

    return y


for i in range(10):
    with open(f'in/{i:02}.in', 'w') as f:
        y = gen()
        print(*y, file=f)
