# Solution
import numpy as np

# 入力の受け取り
x = np.array(list(map(float, input().split())))

# ソフトマックス関数の定義
def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x)

# 出力
print(*softmax(x))
