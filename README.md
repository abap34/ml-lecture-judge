# ml-lecture-judge

機械学習講習会用のオンラインジャッジ.

フロントは React.

ジャッジは Celery + Redis でジョブをキューイングして Docker上で実行して、 Flower で監視.

バックエンドは FastAPI.

```
.
.
├── README.md
├── backend
│   ├── Dockerfile                      # バックエンドサーバ用の Dockerfile
│   ├── Dockerfile.celery               # Celery 用の Dockerfile
│   ├── Dockerfile.executor             # ジャッジのときに実際にコードを実行するコンテナ用の Dockerfile
│   ├── check.py
│   ├── requirements.txt                # バックエンドサーバ用のライブラリ
│   ├── src
│   │   ├── db.py
│   │   ├── executor.py                 # ジャッジの実際の実行のインターフェース
│   │   ├── judge
│   │   │   ├── __init__.py
│   │   │   ├── requirements.txt        # ユーザが使えるライブラリ
│   │   │   └── tasks.py                # Celery 用のタスク
│   │   └── main.py
│   └── static
│       └── problems                    # ここ以下に問題を追加する
│           ├── hello-ml
│           │   ├── description.md
│           │   ├── in
│           │   ├── out
│           │   ├── problem.yaml
│           │   └── solution.py
│           └── helper.py
├── build.sh
├── docker-compose.yaml
└── front
    ├── Dockerfile
    ├── package-lock.json
    ├── package.json
    ├── public
    │   ├── favicon.ico
    │   ├── index.html
    │   ├── manifest.json
    │   └── robots.txt
    └── src
        ├── App.css
        ├── App.js
        ├── App.test.js
        ├── index.css
        ├── index.js
        ├── reportWebVitals.js
        └── setupTests.js

```

## Usage

### セットアップ

`backend/src/judge/requirements.txt` にユーザが使っていいライブラリを追加する。


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
