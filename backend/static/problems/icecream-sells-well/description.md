# 問題文 
アイスクリームの売り上げ $y$ (`'アイスクリーム'`)と気温 $x$ (`'日最高気温の平均(℃)'`)についての問題です。
$$ y = f(x; a, b) = ax + b $$
とします。

$$ L(a, b) = \frac{1}{N} \sum_{i}(y_i − f(x_i; a, b)) ^ 2 $$
を最小にする $a, b$ をPyTorchを用いて勾配降下法を実装することで探索してください。
初期値、学習率、ループの回数を上手く選ぶ必要があります。
モデルの良さ、すなわち最終的な損失の小ささを得点とします。

データは次のリンクからダウンロードできます。(第一回目の講義資料のと同じもの)
https://okumuralab.org/~okumura/stat/data/icecream.csv
https://okumuralab.org/~okumura/stat/data/tokyo-weather-2003-2012.csv

# 入力
なし

# 出力
勾配降下法で探索後の損失関数の値を出力してください。