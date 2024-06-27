# Description
$y = f(x_1, x_2, x_3) = x_1^2 + x_2^2 + x_3^2$ の $x_1 = 1.0, x_2 = 2.0,  x_3=3.0$ における偏微分係数をPyTorchを使って求めてください。
## 入力
なし

## 出力
$x_1, x_2, x_3$ についての偏微分係数をそれぞれ改行区切りで出力してください。
PyTorchで求まる答えは `torch.tensor` オブジェクトになりますが、
出力する際は `.item()` メソッドを用いて数値データのみを取り出して出力してください。

つまり、答えとなる `torch.tensor` オブジェクトを `ans_x1`, `ans_x2`, `ans_x3` とするとき、以下のコードに従うと正しい形式で出力ができます。
```python
print(ans_x1.item())
print(ans_x2.item())
print(ans_x3.item())
```