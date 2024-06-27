# Solution
import torch

# 問題2
x1 = torch.tensor([1.0], requires_grad=True)
x2 = torch.tensor([2.0], requires_grad=True)
x3 = torch.tensor([3.0], requires_grad=True)
y = x1 ** 2 + x2 ** 2 + x3 ** 2
y.backward()
ans_x1 = x1.grad
ans_x2 = x2.grad
ans_x3 = x3.grad

# 回答を出力
print(ans_x1.item())
print(ans_x2.item())
print(ans_x3.item())