# Solution
import torch

# 問題1
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x + 1
y.backward()
ans_x = x.grad

# 問題2
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x[0] ** 2 + x[1] ** 2 + x[2] ** 2
y.backward()
ans_xv = x.grad

# 問題3
W = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], requires_grad=True)
x1 = torch.tensor([[1.0, 2.0]], requires_grad=True)
x2 = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = torch.matmul(torch.matmul(x1, W), x2)
y.backward()
ans_W = W.grad
ans_x1 = x1.grad
ans_x2 = x2.grad

# 回答を出力
print(*ans_x.numpy().flatten().tolist())
print(*ans_xv.numpy().flatten().tolist())
print(*ans_W.numpy().flatten().tolist())
print(*ans_x1.numpy().flatten().tolist())
print(*ans_x2.numpy().flatten().tolist())