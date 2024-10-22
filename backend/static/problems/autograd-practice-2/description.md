$y = f(x_1, x_2, x_3) = x_1^2 + x_2^2 + x_3^2$ の $x_1 = 1, x_2 = 2,  x_3=3$ における偏微分係数をPyTorchを使って求めてください。

## 入力
なし

## 出力
$x_1, x_2, x_3$ についての偏微分係数をそれぞれ改行区切りで出力してください。

例えば、 $x_1, x_2, x_3$ についての偏微分係数が $1.0, 2.0, 3.0$ である場合、次のように出力してください。

```plaintext
1.0
2.0
3.0
```



ここで、通常、勾配はスカラーを保持する `Tensor` 型のオブジェクトとして得られます。

`Tensor` 型のオブジェクトは、 `item` メソッドを用いることで、その中身を取り出すことができます。

そのため `gx1`, `gx2`, `gx3` という変数に答えが格納されている場合、次のようにして出力をすれば正しい形式で出力することができます。

```python
print(gx1.item())
print(gx2.item())
print(gx3.item())
```