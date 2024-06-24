# 
# - $1 \leq n \leq 100$
# - $-1000 \leq y_i \leq 1000$
# - 入力は全て整数

import numpy as np

def gen():
    n = np.random.randint(1, 101)
    y = np.random.randint(-1000, 999, n)

    # y の総和が n の倍数になるように調整
    need = n - (y.sum() % n)

    for i in range(need):
        y[i] += 1
        
    return y


for i in range(10):
    with open(f'in/{i:02}.in', 'w') as f:
        y = gen()
        print(*y, file=f)
