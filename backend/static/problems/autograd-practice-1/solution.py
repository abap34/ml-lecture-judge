# Solution
import torch

# 問題1
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x + 1
y.backward()
ans_x = x.grad

# 回答を出力
print(ans_x.item())