# 問題のつくりかた

問題は `backend/static/problems` 以下に配置されています。

ここに追加する形で問題を作っていってほしいです。


## 問題作成のながれ


### 問題名

まずは問題 id を考えます。

ここでは `mean-squared-error` という問題を作ることにします。 
URLの一部としても使われるので、

- 英小文字, 数字, ハイフンのみ
- 20文字以内

にしてください。

### ブランチを切る

`problems/{問題id}` というブランチを切ってください。

### 問題の雛形を作る.

`helper.py` で問題の雛形を作れます。


```bash
$ python3 helper.py template mean-squared-error
```

これで `backend/static/problems/mean-squared-error` 以下に問題の雛形が作られます。

```bash
$ tree backend/static/problems/mean-squared-error
backend/static/problems/mean-squared-error/
├── description.md
├── in
├── out
├── problem.yaml
└── solution.py
```

各ファイルは、

- `description.md`: 問題文
- `in`: 入力例を入れるディレクトリ
- `out`: 出力例を入れるディレクト
- `problem.yaml`: 問題の設定
- `solution.py`: 解答例

です。　ここからはそれぞれのファイルを編集していきます。

編集対象のファイルは `description.md`, `in/`, `problem.yaml`, `solution.py` です。

### 問題文 (`description.md`)

問題文です。　

markdown で記述してください。

記述のしかたは `backend/static/problems/hello-ml/description.md` を参考にしてください。

### 入力例 (`in/`)

この下に入力例を置いてください。

`in/01.in`, `in/02.in`, ... という名前で置いてください。

### 問題設定 (`problem.yaml`)

ここに問題の設定を書くことができます。

タイトル、得点数、制約などを書いてください。

得点数は問題が出揃ってからこちらで調整するので、まだ適当で大丈夫です。

また、このオンラインジャッジは実行時間などを安定化するための施策をあまりしていないので、
制約はあまり厳しくしないでください。
(手元実行の4倍くらいは確保しておいた方が良さそうです)

誤差ジャッジをしたい場合、　`error_judge` を `true` にして、許容誤差を設定してください。

想定解および真の値を `float` として読み、その絶対誤差または相対誤差が設定された誤差以下であれば正解になります。

```yaml
# 概要
# 概要
summary: 
  title: Hello, AutoGrad!
  points: 100
  
# 制約
constraints:
  # 実行時間制限 (ミリ秒)
  time: 2000
  # メモリ制限 (MB)
  memory: 256
  # 誤差ジャッジをするか？
  error_judge: true
  # 許容絶対誤差
  absolute_error: 1e-5
  # 許容相対誤差
  relative_error: 1e-5
```


### 解答例 (`solution.py`)

ここに正しい解法を書きます。

公開する可能性もあるので、綺麗に (可能なら少しコメントもつけて) 書いてください。

### 正解の生成 

ここまで書けたら、正解を生成します。

```bash
$ python3 helper.py generate mean-squared-error
```

これで `in/` 以下の入力例に対して、解答例を実行した結果が `out/` 以下に生成されます。


## チェック

```bash
$ chmod +x build.sh
$ ./build.sh
$ docker-compose up
```

で `localhost:3000` にアクセスし、左上のメニューから問題を選んで提出して正常に動作するか確認してください。

## Pull Request

ここまで出来たら Pull Request を送って、　@abap34 にレビューをリクエストしてください。

こちらでレビューをするので、通した時点で無事こっちの責任なので安心して送ってください。


