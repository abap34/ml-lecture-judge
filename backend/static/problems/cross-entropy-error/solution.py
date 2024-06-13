# Solution
import numpy as np


def cross_entropy_error(y, t):
    y = np.array(y)  # numpy.ndarrayにしておく。(lossを一片に計算できるため)
    t = np.array(t)
    N = y.shape[0]  # 行列yの行数がバッチサイズであることに注意
    loss = - 1/N * np.sum(t * np.log(y))  # np.sum(...)の部分では成分ごとに tlog(y) 計算しn,kに関して和をとっている。
    return loss


N = int(input())  # バッチサイズを受け取る
y = [list(map(float, input().split(' '))) for _ in range(N)]  # N行分の入力を、各々の値をfloat型にキャストして受け取る。（区切り文字はスペース）
t = [list(map(int, input().split(' '))) for _ in range(N)]
loss = cross_entropy_error(y, t)  # 交差エントロピー誤差を計算
print(loss)
