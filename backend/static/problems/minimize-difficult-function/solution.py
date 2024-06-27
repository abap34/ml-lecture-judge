# Solution
import torch

lr = 0.01

x = float(input())
x = torch.tensor(x, requires_grad=True)


def f(x):
    return -(torch.log(1 / (1 + torch.exp(-x)) + 1))/(x ** 2 + 1)


for i in range(10001):
    y = f(x)
    y.backward()
    with torch.no_grad():
        x = x - lr * x.grad
    x.requires_grad = True

print(x.item())
