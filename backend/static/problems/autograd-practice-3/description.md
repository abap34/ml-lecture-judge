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

ここで、通常、勾配を保持する `Tensor` 型のオブジェクトとして得られます。

`Tensor` 型のオブジェクトは、 `numpy` メソッドを用いることで、その中身を Numpy配列に変換することができます。

そのため `W`, `gx1`, `gx2` という変数に答えが格納されている場合、次のようにして出力をすれば正しい形式で出力することができます。


```python
print(*gW.numpy())
print(*gx1.numpy())
print(*gx2.numpy())
``` 