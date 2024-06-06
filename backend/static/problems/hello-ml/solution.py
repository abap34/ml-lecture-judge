# Solution
import torch

# f を定義
f = eval(input())

# x を定義
x = torch.tensor(float(input()), requires_grad=True)

# y を計算
y = f(x)

y.backward()

# x.grad を小数点以下 3 桁まで出力
print(round(x.grad.item(), 3))
