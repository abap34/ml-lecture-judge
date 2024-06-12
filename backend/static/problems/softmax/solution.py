# Solution
import numpy as np

# 入力の受け取り
x = np.array(list(map(float, input().split())))

# ソフトマックス関数の定義
def softmax(x):
    return np.exp(x) / np.sum(np.exp(x))

# 出力
print(*softmax(x))
