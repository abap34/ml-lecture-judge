過学習に対する措置として正則化がある．正則化ではコスト関数に正則化項を加えることで過学習を抑えることができる．正則化項には有名なものとして重みのノルムを用いたL1正則化や，その2乗を用いたL2正則化がある．$\lambda$は正則化パラメータと呼ばれる．L2正則化ではコスト関数を$w$で微分した時に扱いやすいように，$\lambda/2$を正則化項とすることが多い．

予測値として$\hat{\bm{y}}\in \mathbb{R}^{t}$，実測値として$\bm{y} \in \mathbb{R}^{t}$が与えられているとする．この時$\bm{y}$はone-hotエンコンディング表現で$t\times 1$次元となっている．
(例)
$$
\hat{\bm{y}} = \begin{pmatrix}0.2\\0.1\\0.9\\\vdots\end{pmatrix}, \bm{y}=\begin{pmatrix}0\\0\\1\\\vdots\end{pmatrix}
$$

この時コスト関数が正則化項$\lambda\|\bm{w}\|^2/2$（$\bm{w}$は重み）を加えて
$$
J(\bm{w})=-\left(-\sum_{j=1}^t y_j\log(\hat{y}_j)+ (1-y_j)\log(1-\hat{y}_j)\right)+\frac{\lambda}{2}\|\bm{w}\|^2
$$
であたえられるとする．

これを元に，$\bm{x}\in\mathbb{R}^m$，$\bm{y}\in \mathbb{R}^{t}$が与えられ，それに対する予測値が$\hat{\bm{y}}=\text{softmax}(\bm{w}\bm{x})$で定義される時，$\lambda=1$として正則化項を加えたコスト関数の最小値を求めよ．ただし$\bm{w}$の初期値は$\bm{0}$とする．

## 制約
- $1 \leq m \leq 20$
- $1 \leq t \leq 5$
- $-100 \leq x_i\leq 100$ ($1 \leq i \leq m$)
- $y_i \in \{0, 1\}$

## 入力
入力は以下の形式で標準入力から与えられます。

```plaintext
m t
x_1 x_2 ... x_m
y_1 y_2 ... y_t
```
従って以下のコードで入力を受け取れます．
```python3
m, t = map(int, input().split())
x = torch.tensor(list(map(float, input().split()))).reshape(-1,1)
y = torch.tensor(list(map(int, input().split()))).reshape(-1, 1)
```
## 出力
最小化された$J(\bm{w})$を出力してください．想定界との絶対誤差が$10^{-3}$以下の時に正解と判定されます．
```plaintext
J_w
```

## サンプル
### サンプル1
#### 入力
```plaintext
4 3
0 1 2 3
0 1 0
```

#### 出力
```plaintext
0.39896008372306824
```
### サンプル2
#### 入力
```plaintext
6 4
1 3 2 4 3 5
0 1 0 0
```
#### 出力
```plaintext
0.1829862892627716
```