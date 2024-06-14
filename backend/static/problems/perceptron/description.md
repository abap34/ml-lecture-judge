$\boldsymbol{x} \in \R^n$, $\boldsymbol{w} \in \R^n$, $b \in \R$ が与えられます。

次の値を計算し出力してください。

$$
\boldsymbol{w}^T \cdot \boldsymbol{x} + b
$$

- $\boldsymbol{w}^T$ は $\boldsymbol{w}$ の転置ベクトルを表します。
- $\boldsymbol{w}^T \cdot \boldsymbol{x}$ は $\boldsymbol{w}^T$ と $\boldsymbol{x}$ の内積を表します。

## 制約
- $1 \leq n \leq 20$
- $-100 \leq \boldsymbol{x}_i, \boldsymbol{w}_i \leq 100$ ($1 \leq i \leq n$)
- $-100 \leq b \leq 100$
- 入力はすべて小数

## 入力
入力は以下の形式で標準入力から与えられます。

$
\boldsymbol{x}_1 \ \boldsymbol{x}_2 \ \ldots \ \boldsymbol{x}_n
\newline
\boldsymbol{w}_1 \ \boldsymbol{w}_2 \ \ldots \ \boldsymbol{w}_n
\newline
b
$

従って以下のコードで入力を受け取ることができます。
```python3
x = np.array(list(map(float, input().split())))
w = np.array(list(map(float, input().split())))
b = float(input())
```

## 出力
計算結果 $y \in \R$ を出力してください。

想定解との絶対誤差または相対誤差が $10^{-3}$ 以下であれば正解とします。

## サンプル
### サンプル1
#### 入力
```plaintext
1.0 2.0 3.0
0.1 0.2 0.3
0.4
```

#### 出力
```plaintext
1.8
```
