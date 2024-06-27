$f(\bm{x_1}, \bm{x_2}, W) = \bm{x_1}^T W \bm{x_2}$ の

$W = \begin{pmatrix}
1 & 3 & 5 \\
2 & 4 & 6 
\end{pmatrix}$, $\boldsymbol{x}_1 = (1.0, 2.0)^T, \boldsymbol{x}_2 = (1.0,2.0,3.0)^T$ における勾配をそれぞれ求めてください。

なお、`torch.matmul(A, B)` によって `A` と `B` の行列積を計算できます。

## 入力
なし

## 出力
$W$ 、$\boldsymbol{x}_1$、$\boldsymbol{x}_2$ についての勾配をそれぞれ改行区切りで出力してください。
PyTorchで求まるそれぞれの勾配は `torch.tensor` オブジェクトになりますが、
出力する際は `.flatten()` メソッドを用いてそれぞれの配列を一次元の配列に変換したうえで、その配列の要素を空白区切りで出力してください。

つまり、この問題の答えがそれぞれ `gW`, `gx1`, `gx2` に格納されているとき、次のようにすると正しい出力になります。

```python
print(*gW.flatten().numpy())
print(*gx1.flatten().numpy())
print(*gx2.flatten().numpy())
``` 