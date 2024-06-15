ソフトマックス関数 $\sigma: {\R}^n \rarr {\R}^n$ を以下のように定義します。

$$
\sigma(\boldsymbol{x})_i = \frac{\exp(\boldsymbol{x}_i)}{\sum_{j=1}^{n} \exp(\boldsymbol{x}_j)} 
$$

- $\sigma(\boldsymbol{x})_i$ は $\sigma(\boldsymbol{x})$ の $i$ 番目の要素を表します。

ベクトル $\boldsymbol{x} \in {\R}^{n}$ が与えられるので $\sigma(\boldsymbol{x})$ の値を計算する関数をnumpyを用いて実装し $\sigma(\boldsymbol{x})$ を計算し出力してください。$\exp(\boldsymbol{x}_i)$ の値が**非常に大きくなりオーバーフローを引き起こす**場合があることに注意してください。想定解ではこの問題に対して適切な処理を行っています。

## 制約
- $1 \leq n \leq 10$
- $|\boldsymbol{x}_i| \leq 1000$ $(1\leq i \leq n)$
- 入力は全て小数


## 入力
ベクトル $\boldsymbol{x}$ は以下の形式で標準入力から与えられます。
 
$$
\boldsymbol{x}_1 \ \boldsymbol{x}_2 \ \ldots \ \boldsymbol{x}_{n}
$$



したがって以下のようなコードで $\boldsymbol{x}$ を1次元numpy配列として定義することができます。

```python3
x = np.array(list(map(float, input().split())))
```
## 出力
計算結果 $\sigma(\boldsymbol{x})$ を以下のように空白区切りで出力してください。
$$
\sigma(\boldsymbol{x})_1 \ \sigma(\boldsymbol{x})_2 \ \ldots \ \sigma(\boldsymbol{x})_{n}
$$

出力は全ての要素について想定解との絶対誤差または相対誤差が $10^{-3}$ 以下のとき正解と判定されされます。

1次元numpy配列 $x$ を空白区切りで出力するには以下のようにして出力することもできます。

```python3
print(*x)
```

## サンプル

### サンプル1

#### 入力
```plaintext
1.0 2.0 3.0
```

#### 出力
```plaintext
0.09003057317038046 0.24472847105479767 0.6652409557748219
```

### サンプル2
#### 入力
```plaintext
1.2 777.0 774.9
```

#### 出力
```plaintext
0 0.89090318 0.10909682
```
