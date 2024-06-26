この問題は三つの小問題からなります。

### 問題1
 $y = x^2 + 2x + 1$ の $x=3.0$ における微分係数をPyTorchを使って求めてください。


### 問題2
2. $y = f(\boldsymbol{x}) = x_1^2 + x_2^2 + x_3^2$ の $\boldsymbol{x}=(1.0, 2.0, 3.0)^T$ における勾配をPyTorchを使って求めてください。

### 問題3
3. $W = (\begin{array}{ccc}
1.0 & 2.0 & 3.0 \cr
4.0 & 5.0 & 6.0 \end{array}), \boldsymbol{x}_1 = (1.0, 2.0), \boldsymbol{x}_2 = (1.0,2.0,3.0)^T$について、$y = \boldsymbol{x}_1 W \boldsymbol{x}_2$ の勾配をPyTorchを使って求めてください。

なお、横ベクトルは形状が(1, n)の行列、縦ベクトルは形状が(n, 1)の行列としてPyTorch上で扱ってください。
PyTorchにおいて、行列積は`torch.matmul`を使って計算できます。

## 入力

なし

## 出力
問題1, 2, 3の答えはそれぞれある形状を持った`torch.tensor`オブジェクトとなります。それぞれ一次元リストに変換し、要素を空白区切りで出力してください。答えと答えの間には改行を入れてください。  
つまり、問題1の答えが`ans_x`、問題2の答えが`ans_xv`、問題3の答えが`ans_W`、`ans_x1`、`ans_x2`であるとき、以下のコードを用いると正しい形式で出力ができます。
```python
print(*ans_x.numpy().flatten().tolist())
print(*ans_xv.numpy().flatten().tolist())
print(*ans_W.numpy().flatten().tolist())
print(*ans_x1.numpy().flatten().tolist())
print(*ans_x2.numpy().flatten().tolist())
```