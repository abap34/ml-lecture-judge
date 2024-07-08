# Solution
import torch

# 入力の受け取り
m, t = map(int, input().split())
x = torch.tensor(list(map(float, input().split()))).reshape(-1,1)
y = torch.tensor(list(map(int, input().split()))).reshape(-1, 1)

# パラメータの初期化
w = torch.zeros((t,m), requires_grad=True)

# 最小化
for i in range(100):
    pred = torch.softmax(torch.matmul(w, x), dim=0)
    J_w = -torch.sum(y * torch.log(pred) + (1-y) * torch.log(1-pred)) + 0.5 * torch.norm(w)**2
    J_w.backward()
    with torch.no_grad():
        w -= 0.1 * w.grad
        w.grad.zero_()
# 出力
print(J_w.item())
