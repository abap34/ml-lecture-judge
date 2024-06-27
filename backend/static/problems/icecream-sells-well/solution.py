# Solution
import pandas as pd
import torch

icecream = pd.read_csv('icecream.csv', encoding='shift_jis', header=1)
weather = pd.read_csv('tokyo-weather-2003-2012.csv', encoding='shift_jis')
x, t = weather['日最高気温の平均(℃)'], icecream['アイスクリーム']
x = torch.tensor(x.values)
t = torch.tensor(t.values)
n = len(x)

def mean_squared_error(y, y_pred):
    return torch.sum((y - y_pred) ** 2) / n

def loss(a, b):
    pred = a * x + b
    return mean_squared_error(t, pred)

lr = 0.001
N = 100001
a = torch.tensor(50.0, requires_grad=True)
b = torch.tensor(-250.0, requires_grad=True)

loss_trace = []
for i in range(N):
    L = loss(a, b)
    L.backward()
    with torch.no_grad():
        a = a - lr * a.grad
        b = b - lr * b.grad

    a.requires_grad = True
    b.requires_grad = True
    if i % 1000 == 0:
        loss_trace.append(L.item())


print(loss_trace[-1])
