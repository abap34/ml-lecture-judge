# Solution
import numpy as np


# 数値微分で勾配を計算する関数
def numerical_grad(f, x, h=1e-5):
    grad = np.zeros_like(x)
    for i in range(x.size):
        tmp = x[i]
        x[i] = tmp + h
        fx2 = f(x)
        x[i] = tmp - h
        fx1 = f(x)
        grad[i] = (fx2 - fx1) / (2 * h)
        x[i] = tmp
    return grad


class Adam:
    def __init__(self, alpha=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None
        self.v = None
        self.unbiased_m = None
        self.unbiased_v = None
        self.iter = 0

    def update(self, param, grad):
        if self.m is None:
            self.m = np.zeros_like(grad)
            self.v = np.zeros_like(grad)
        self.iter += 1
        self.m = self.beta1 * self.m + (1.0 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1.0 - self.beta2) * (grad ** 2)
        self.unbiased_m = self.m / (1.0 - self.beta1 ** self.iter)
        self.unbiased_v = self.v / (1.0 - self.beta2 ** self.iter)
        delta_w = - self.alpha * self.unbiased_m / (np.sqrt(self.unbiased_v) + self.epsilon)
        param += delta_w


# Matyas Functionと呼ばれる最適化のテスト用の関数
def L(w):
    x, y = w
    z = 0.26 + (x ** 2 + y ** 2) + 0.48 * x * y
    return z


N = int(input())
w = np.array(list(map(float, input().split())))
w_grad = np.zeros_like(w)
optimizer = Adam()

for i in range(N):
    z = L(w)
    w_grad = numerical_grad(L, w)
    optimizer.update(w, w_grad)

print(*w)
