# ml-lecture-judge

機械学習講習会用のオンラインジャッジ.

フロントは React + Material-UI.
ジャッジは Celery + Redis + Docker. 
ジョブの監視は Flower. 

## Usage

### セットアップ

`src/executor/requirements.txt` にジャッジで必要なライブラリを記述する。

問題を追加する。

```bash
$ python3 problems/helper.py gen {problem_name}
```

で問題の雛形を生成する。 input, solution, output を記述する。

```bash
$ python3 problems/helper.py genout {problem_name}
```

で出力を生成する。


### ビルド

```bash
$ ./build.sh
```

### 起動

```bash
$ docker-compose up 
```

- `http://localhost:3000` (front)
- `http://localhost:8000` (back)
- `http://localhost:5555` (flower)


### 終了

```bash
$ docker-compose down
```
