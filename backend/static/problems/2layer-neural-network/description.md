入力層、1層の中間層、出力層からなる2層のニューラルネットワークをnumpyを用いて実装してみましょう。

ニューラルネットワークへの入力 $\bold{x} \in \R^n$ ,第1層の重みパラメータ $\bold{W}^{(1)} \in \R^{m \times n}$ 、第1層のバイアスパラメータ $\bold{b}_1 \in \R^m$, 第2層の重みパラメータ $\bold{W}^{(2)} \in \R^{k \times m}$, 第2層のバイアスパラメータ $\bold{b}_2 \in \R^k$ が与えられます。

中間層の活性化関数はReLU関数、出力層の活性化関数は恒等関数とします。

このニューラルネットワークの出力 $\bold{y} \in \R^k$ を計算してください。

## 制約
- $1 \leq n, m, k \leq 100$
- $-100 \leq \bold{x}_i, \bold{W}_{i,j}^{(1)},\bold{W}_{i,j}^{(2)}, \bold{b}_i^{(1)}, \bold{b}_i^{(2)} \leq 100$
- 入力は全て整数

## 入力
入力は以下の形式で標準入力から与えられます。

$
n \ m \ k \\
\bold{x}_1 \ \bold{x}_2 \ \ldots \ \bold{x}_n \\
\bold{W}_{11}^{(1)} \ \bold{W}_{12}^{(1)} \ \ldots \ \bold{W}_{1n}^{(1)} \\
\bold{W}_{21}^{(1)} \ \bold{W}_{22}^{(1)} \ \ldots \ \bold{W}_{2n}^{(1)} \\
\vdots \\
\bold{W}_{m1}^{(1)} \ \bold{W}_{m2}^{(1)} \ \ldots \ \bold{W}_{mn}^{(1)} \\
\bold{b}_1^{(1)} \ \bold{b}_2^{(1)} \ \ldots \ \bold{b}_m^{(1)} \\
\bold{W}_{11}^{(2)} \ \bold{W}_{12}^{(2)} \ \ldots \ \bold{W}_{1m}^{(2)} \\
\bold{W}_{21}^{(2)} \ \bold{W}_{22}^{(2)} \ \ldots \ \bold{W}_{2m}^{(2)} \\
\vdots \\
\bold{W}_{k1}^{(2)} \ \bold{W}_{k2}^{(2)} \ \ldots \ \bold{W}_{km}^{(2)} \\
\bold{b}_1^{(2)} \ \bold{b}_2^{(2)} \ \ldots \ \bold{b}_k^{(2)} \\
$

したがって以下のようなコードで入力を受け取ることができます。

```python3
n, m, k = map(int, input().split())
x = np.array(list(map(int, input().split())))
W1 = np.array([list(map(int, input().split())) for _ in range(m)])
b1 = np.array(list(map(int, input().split())))
W2 = np.array([list(map(int, input().split())) for _ in range(k)])
b2 = np.array(list(map(int, input().split()))
```
## 出力
出力 $\bold{y} \in \R^k$ の要素を空白区切りで出力してください。

## サンプル

### サンプル1

#### 入力
```plaintext
3 2 2
2 -4 3
4 -4 2
3 -2 0
-4 -1
-2 2
3 -5
2 -4
```

#### 出力
```plaintext
-24 9
```

### サンプル2

#### 入力
```plaintext
10 5 2
79 -23 -9 -25 10 49 13 -41 26 58
-63 -83 -92 -95 4 -4 54 -48 15 55
86 53 -24 80 -70 76 35 -51 -48 40
98 89 -8 -48 -11 -1 -69 88 -96 -58
-18 -93 -61 -56 70 -56 -16 65 -70 29
-95 -44 -20 -68 -41 52 -16 29 32 -9
12 74 62 -97 -42
2 -24 40 58 25
-31 57 56 -24 40
-49 -83
```

#### 出力
```plaintext
-239735 405345
```