# Description
$y = f(\boldsymbol{x}) = x_1^2 + x_2^2 + x_3^2$ の $\boldsymbol{x}=(1.0, 2.0, 3.0)^T$ における勾配をPyTorchを使って求めてください。

## 入力
なし

## 出力
この問題の答えは形状 $(3, 1)$ の `torch.tensor` オブジェクトになりますが、
出力する際は `.flatten()` メソッドを用いて一次元の配列に変換したうえで、その配列の要素を空白区切りで出力してください。

つまり、答えとなる `torch.tensor` オブジェクトを `ans_x` とするとき、以下のコードに従うと正しい形式で出力ができます。
```python
print(*ans_xv.numpy().flatten().tolist())
```