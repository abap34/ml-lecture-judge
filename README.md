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

`.env` に以下の情報をおく

```plaintext
TRAQ_CLIENT_ID=
TRAQ_CLIENT_SECRET=
SECRET_KEY=
API_URL=
FRONT_URL=
CURRENT_SECTION=
```

`CURRENT_SECTION` より小さい問題だけが見えます。


### ビルド (全部)

```bash
$ ./build.sh
```

### 起動

```bash
$ docker-compose up 
```

### バックエンドだけビルドと起動

```bash
$ chomod +x deploy-back.sh
$ ./deploy-back.sh
```



- `http://localhost:3000` (front)
- `http://localhost:8000` (back)
  - `http://localhost:8000/docs` (Swagger)
- `http://localhost:5555` (flower)


### 終了

```bash
$ docker-compose down
```
