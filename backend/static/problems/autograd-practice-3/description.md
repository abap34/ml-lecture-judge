# Description
3. $W = (\begin{array}{ccc}
1.0 & 2.0 & 3.0 \cr
4.0 & 5.0 & 6.0 \end{array}), \boldsymbol{x}_1 = (1.0, 2.0), \boldsymbol{x}_2 = (1.0,2.0,3.0)^T$について、$y = \boldsymbol{x}_1 W \boldsymbol{x}_2$ の勾配をPyTorchを使って求めてください。

なお、横ベクトルは形状が(1, n)の行列、縦ベクトルは形状が(n, 1)の行列としてPyTorch上で扱ってください。
PyTorchにおいて、行列積は`torch.matmul`を使って計算できます。

## 入力
なし

## 出力
$W$ 、$\boldsymbol{x}_1$、$\boldsymbol{x}_2$ についての勾配をそれぞれ改行区切りで出力してください。
PyTorchで求まるそれぞれの勾配は `torch.tensor` オブジェクトになりますが、
出力する際は `.flatten()` メソッドを用いてそれぞれの配列を一次元の配列に変換したうえで、その配列の要素を空白区切りで出力してください。
この問題の答えをそれぞれ `ans_W`, `ans_x1`, `ans_x2` とするとき、以下のコードに従うと正しい形式で出力ができます。
```python
print(*ans_W.flatten().numpy())
print(*ans_x1.flatten().numpy())
print(*ans_x2.flatten().numpy())
``` 