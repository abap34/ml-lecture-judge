※ この問題はサンプル問題です。

<details>
<summary>解答</summary>

```
import torch

f = eval(input())

x = torch.tensor(float(input()), requires_grad=True)

y = f(x)

y.backward()

print(x.grad.item())
```

</details>



関数 $f: \mathbb{R} \to \mathbb{R}$ と 実数 $x$ が与えられます。

$f'(x)$ を求めて出力してください。

## 制約

- $f(x)$ は PyTorch でサポートされている関数のみからなります。
- $f(x)$ は $x$ に関する微分可能な関数です。
- $-10^3 \leq x \leq 10^3$
- $-10^3 \leq f(x) \leq 10^3$

## 入力

```plaintext
f
x
```

- $f$ は $x$ に対する関数 $f(x)$ を表す式で、
  ```python3
  lambda x: {xの式}
  ```

  という形で書かれています。

  したがって、以下のようなコードで $f$ を定義することができます。

  ```python3
  f = eval(input())
  ```

  ここで `{xの式}` は PyTorch でサポートされている関数のみからなり、返り値は `x` と計算グラフ上で繋がっている `torch.Tensor` であることが保証されています。

## 出力

$f'(x)$ の値を出力してください。

想定解との絶対誤差または相対誤差が $10^{-3}$ 以下であれば正解となります。

ここで、想定解と真の値の絶対誤差または相対誤差は $10^{-8}$ 以下であることが保証されています。

## サンプル

### サンプル1

#### 入力
```plaintext
lambda x: x**2
1.0
```

#### 出力
```plaintext
2.000
```

### サンプル2

#### 入力
```plaintext
lambda x: torch.cos(x * 3.14159265358979323846)
0.0
```

#### 出力
```plaintext
-0.000
```





