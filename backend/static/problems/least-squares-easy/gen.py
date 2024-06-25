# n は整数
# 2 <= n <= 50
# -10 <= x_i, y_i <= 10

import numpy as np  

def gen():
    n = np.random.randint(2, 51)
    x = np.random.uniform(-10, 10, n)
    y = np.random.uniform(-10, 10, n)

    return n, x, y

for i in range(3, 10):
    with open('in/{:02d}.in'.format(i), 'w') as f:
        n, x, y = gen()
        f.write(f'{n}\n')
        f.write(' '.join(map(str, x)) + '\n')
        f.write(' '.join(map(str, y)) + '\n')

