# ユーザテーブル (`users`)
ユーザに関する情報を格納します。

- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
  - ユーザの一意識別子。
- `username`: TEXT, NOT NULL, UNIQUE
  - ユーザ名。
- `email`: TEXT, NOT NULL, UNIQUE
  - メールアドレス。
- `password_hash`: TEXT, NOT NULL
  - パスワードのハッシュ。
- `created_at`: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
  - アカウント作成日時。
- `updated_at`: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
  - アカウント更新日時。

# チームテーブル (`teams`)
チームに関する情報を格納します。

- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
  - チームの一意識別子。
- `name`: TEXT, NOT NULL, UNIQUE
  - チーム名。
- `created_at`: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
  - チーム作成日時。
- `updated_at`: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
  - チーム更新日時。

# ユーザ・チームの関連テーブル (`team_members`)
ユーザとチームの関連情報を格納します。

- `user_id`: INTEGER, NOT NULL, FOREIGN KEY REFERENCES `users`(id) ON DELETE CASCADE
  - ユーザの一意識別子。
- `team_id`: INTEGER, NOT NULL, FOREIGN KEY REFERENCES `teams`(id) ON DELETE CASCADE
  - チームの一意識別子。
- `joined_at`: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
  - 参加日時。
- PRIMARY KEY (`user_id`, `team_id`)
  - ユーザとチームの組み合わせを一意に識別します。


# 提出物テーブル (`submissions`)
提出されたコードに関する情報を格納します。

- `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
  - 提出物の一意識別子。
- `problem_id`: INTEGER, NOT NULL, FOREIGN KEY REFERENCES `problems`(id) ON DELETE CASCADE
  - 問題の一意識別子。
- `user_id`: INTEGER, NOT NULL, FOREIGN KEY REFERENCES `users`(id) ON DELETE CASCADE
  - ユーザの一意識別子。
- `team_id`: INTEGER, FOREIGN KEY REFERENCES `teams`(id) ON DELETE SET NULL
  - チームの一意識別子。
- `code`: TEXT, NOT NULL
  - 提出されたコード。
- `status`: TEXT
  - 判定結果（例: "Accepted", "Wrong Answer", "Runtime Error"）。
- `submitted_at`: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
  - 提出日時。
