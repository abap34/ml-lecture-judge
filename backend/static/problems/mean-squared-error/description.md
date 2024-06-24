回帰問題において損失関数としてよく用いられる二乗誤差 (Mean Squared Error)をPythonの外部ライブラリであるnumpyを用いて実装してみましょう。

入力 $x \in \R$ から $y \in \R$ を予測する問題を考えます。予測モデルとして $f(x;a,b) = ax + b \ (a,b\in \R)$ というモデルを用いることにします。

パラメータ $a, b$ とデータ $D = \{(x_1, y_1), (x_2, y_2), \ldots, (x_n, y_n)\}$ が与えられるのでモデル $f(x;a,b)$ の評価として**二乗誤差の合計** $L \in \R$ を計算してください。

$$

L = \sum_{i=1}^{n} (f(x_i;a,b) - y_i)^2

$$

## 制約

- $1 \leq n \leq 100$
- $-10 \leq a, b \leq 10$
- $-1000 \leq x_i, y_i \leq 1000$
- 入力は全て整数

## 入力
入力は以下の形式で標準入力から与えられる。

$
a \ b \\
x_1 \ x_2 \cdots x_n \\
y_1 \ y_2 \cdots y_n
$

したがって以下のようなコードで入力を受け取ることができます。

```python3
a, b = map(int, input().split())
x = np.arrray(list(map(int, input().split())))
y = np.arrray(list(map(int, input().split())))
```


## 出力
**二乗誤差の合計** $L$ を出力してください。

## サンプル
### サンプル1
#### 入力
```
3 2
1 2 3
4 6 12
```
#### 出力
```
6
```