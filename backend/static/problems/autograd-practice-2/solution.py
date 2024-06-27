# Solution
import torch

# 問題2
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x[0] ** 2 + x[1] ** 2 + x[2] ** 2
y.backward()
ans_x = x.grad

# 回答を出力
print(*ans_x.numpy().flatten().tolist())