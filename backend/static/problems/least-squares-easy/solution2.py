import numpy as np

# 入力を受け取る
n = int(input())
x = np.array(list(map(float, input().split())))
y = np.array(list(map(float, input().split())))

# パラメータの初期化
a = 0.0

# 学習率
eta = 0.01

# 最大イテレーション数
max_iter = 10000

# 勾配降下法
for iteration in range(max_iter):
    # 勾配の計算
    gradient = -2/n * np.sum(x * (y - a * x))
    
    # パラメータの更新
    a = a - eta * gradient


# 最小化された平均二乗誤差 L(a)
L_hat_a = np.mean((y - a * x)**2)

print(L_hat_a)
