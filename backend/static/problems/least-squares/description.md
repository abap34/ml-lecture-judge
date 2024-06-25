$\boldsymbol{x} \in \mathbb{R}^n$ と $\boldsymbol{y} \in \mathbb{R}^n$ が与えられます。

$y_i$ を、パラメータ $a \in \mathbb{R}, b \in \mathbb{R}$ を用いてモデル $f(x_i; a, b) = a + b x_i$ で予測することを考えます。

平均二乗誤差 $L$ を最小にする $a, b$ を $\hat{a}, \hat{b}$ とします。 $L(\hat{a}, \hat{b})$ を出力してください。

<span style="color: red; "> ※この問題は、勾配降下法で解くことを想定していません。
</span>

<details>
<summary>ヒント</summary>
実は線形回帰は、講義で紹介した二次関数の最小化と同じように、直接最小値を与えるパラメータを計算することができます。
まずはこの式を導出してプログラムに落とし込んでみましょう。
</details>

## 制約

- $n$ は整数
- $2 \leq n \leq 50$
- $-10^3 \leq x_i, y_i \leq 10^3$
- $\bar{x} = \dfrac{1}{n} \displaystyle \sum_{k=1}^{n} x_i$ とするとき、$\displaystyle \sum_{k=1}^{n} (x_i - \bar{x}) \ne 0$ 

## 入力
入力は以下の形式で標準入力から与えられます。

```plaintext
n
x_1 x_2 ... x_n
y_1 y_2 ... y_n
```

したがって、以下のようなコードで入力を受け取ることができます。

```python3
n = int(input())
x = np.array(list(map(float, input().split())))
y = np.array(list(map(float, input().split())))
```


## 出力

$L(\hat{a}, \hat{b})$ を出力してください。

想定解との相対誤差または絶対誤差が $10^{-2}$ 以下であれば正解とします。

ここで、想定解と真の値の絶対誤差または相対誤差は $10^{-5}$ 以下であることが保証されています。

## サンプル



### サンプル1

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
