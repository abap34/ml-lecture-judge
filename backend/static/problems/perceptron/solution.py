# Solution
import numpy as np

# 入力の受け取り
x = np.array(list(map(float, input().split())))
w = np.array(list(map(float, input().split())))
b = float(input())

# 計算
y = np.dot(w, x) + b

# 出力
print(y)