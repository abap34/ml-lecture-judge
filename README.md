# ml-lecture-judge

機械学習講習会用のオンラインジャッジ.

フロントは React.

ジャッジは Celery + Redis でジョブをキューイングして Docker上で実行して、 Flower で監視.

バックエンドは FastAPI + SQLAlchemy + SQLite.

## Usage

### セットアップ

#### 実行環境のセットアップ

`backend/Docker.executor` が実際に実行に使うコンテナ。
ここで必要なパッケージのセットアップをする。

#### 問題の作成

`notes/PROBLEM_CREATION.md` を参考に問題を作成する。


### 最初にすること

```bash
$ chmod +x build.sh
$ cd front
$ npm install
```


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
  - `http://localhost:8000/docs` (Swagger)
- `http://localhost:5555` (flower)


### 終了

```bash
$ docker-compose down
```
