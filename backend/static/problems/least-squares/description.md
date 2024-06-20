要素数$n$のベクトル $\mathbb{x}$ と $\mathbb{y}$ が与えられます。
$y_i$ を直線 $\alpha + \beta x_i$ で近似することを考えます。
$L(\alpha, \beta) = \dfrac{1}{n} \sum_{k=1}^{n} (y_i - \alpha - \beta x_i)^2$ を最小化する $\alpha, \beta$ を $\hat{\alpha}, \hat{\beta}$ とするとき、近似結果の平均二乗誤差 $ \dfrac{1}{n} \sum_{k=1}^{n} (y_i - \hat{\alpha} - \hat{\beta}x_i)^2 $ を出力してください。
相対誤差または絶対誤差が $10^{-2}$ 以下であれば正解とします。

<details>
<summary>ヒント</summary>

勾配降下法だと時間がかかるので、$\alpha, \beta$ について$L(\alpha, \beta)$ を偏微分して、それぞれの偏微分が0になるような $\alpha, \beta$ を求めましょう。

</details>

## 制約

- $2 \leq n \leq 50$
- $-10^3 \leq x_i, y_i \leq 10^3$

$n$ は整数です。
$\bar{x} = \dfrac{1}{n} \sum_{k=1}^{n} x_i$ とするとき、
$\sum_{k=1}^{n} (x_i - \bar{x}) \ne 0$ であることが保証されています。

## 入力

```plaintext
n
y_1 y_2 ... y_n
x_1 x_2 ... x_n
```

## 出力

求めた $\hat{\alpha}, \hat{\beta}$ について、近似結果の平均二乗誤差を出力してください。

## サンプル



### サンプル2

#### 入力
```plaintext
6
-0.5 0.75 2.0 2.3 3.0 3.75
0.0 1.0 2.0 3.0 4.0 5.0

```

#### 出力
```plaintext
0.07367
```
相対誤差または絶対誤差が $10^{-2}$ 以下であれば正解とします。

### サンプル2

#### 入力
```plaintext
5
1.0 2.0 3.0 4.0 5.0
1.0 2.0 3.0 4.0 5.0
```

#### 出力
```plaintext
0.0
```