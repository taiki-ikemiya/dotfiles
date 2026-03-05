# Conventional Commits v1.0.0 詳細ルール

Conventional Commits は、コミットメッセージに人間と機械が読める意味を付与するための規約である。

---

## メッセージ構造

```
<type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

---

## type 一覧

### 必須 type

| type | 説明 | SemVer との対応 |
|------|------|-----------------|
| feat | 新しい機能の追加 | MINOR |
| fix | バグの修正 | PATCH |

### 推奨 type

| type | 説明 |
|------|------|
| refactor | 機能追加でもバグ修正でもないコード変更 |
| docs | ドキュメントのみの変更 |
| test | テストの追加や既存テストの修正 |
| chore | ビルドプロセスや補助ツール、ライブラリの変更 |
| style | コードの意味に影響しない変更（空白、フォーマット、セミコロン等） |
| perf | パフォーマンスを向上させるコード変更 |
| ci | CI 設定ファイルやスクリプトの変更 |
| build | ビルドシステムや外部依存関係に影響する変更 |
| revert | 以前のコミットを取り消す変更 |

---

## scope 規約

### scope の役割

変更が影響するコードベースのセクションを示す名詞を括弧で囲んで記述する。

### 記述ルール

- 小文字で記述する
- ハイフン区切りを使用する（キャメルケースは避ける）
- モジュール名、ディレクトリ名、機能名を使用する
- 省略してもよい

### scope の例

```
feat(auth): ログイン機能を追加
fix(user-profile): アバター画像の表示崩れを修正
refactor(api-client): HTTPクライアントを抽象化
docs(readme): インストール手順を更新
test(payment): 決済処理のE2Eテストを追加
chore(deps): パッケージの依存関係を更新
```

### 複数 scope にまたがる場合

- 最も影響の大きいモジュールを scope にする
- または scope を省略する
- 複数の scope をカンマ区切りにしない（分割を検討する）

---

## subject の書き方

### ルール

- 50文字以内に収める
- 現在形で記述する（「追加した」ではなく「追加する」「追加」）
- 英語の場合: 先頭を大文字にしない、末尾にピリオドを付けない
- 日本語の場合: 体言止めまたは動詞の終止形で終える
- 命令形（英語）または説明的な表現（日本語）を使用する

### 良い例

```
feat(auth): JWT認証を実装
fix(api): nullレスポンスのハンドリングを修正
refactor(db): クエリビルダーを共通化
```

```
feat(auth): implement JWT authentication
fix(api): handle null response in user endpoint
refactor(db): extract common query builder
```

### 悪い例

```
feat(auth): JWT認証を実装しました。        # 「しました」「。」は不要
fix: いろいろ修正                           # 具体性がない
update                                      # type がない
feat(auth): JWT認証を実装 fix(api): null修正 # 複数の変更を1行に書かない
```

---

## body の書き方

### いつ body を書くか

- subject だけでは変更の理由が伝わらない場合
- 複雑な変更で補足説明が必要な場合
- Breaking Change を含む場合
- 設計判断の背景を記録したい場合

### ルール

- subject との間に1行の空行を入れる
- 72文字で折り返す
- 「何を」変更したかと「なぜ」変更したかを説明する
- 箇条書きを使用してよい（`-` または `*` を使用する）

### body の例

```
feat(auth): JWT認証を実装

セッションベースの認証からJWTベースに移行する。
以下の理由による:
- マイクロサービス間での認証情報の共有が容易になる
- ステートレスな設計によりスケーラビリティが向上する
- モバイルアプリとの認証統合が簡単になる

アクセストークンの有効期限は15分、
リフレッシュトークンの有効期限は7日に設定した。
```

---

## footer の書き方

### Breaking Change

互換性のない変更を含む場合、footer に `BREAKING CHANGE:` を記述する。

```
feat(api): レスポンス形式をJSONAPIに変更

APIレスポンスの形式をJSONAPI仕様に準拠させる。

BREAKING CHANGE: レスポンスのトップレベル構造が変更された。
従来の { data: [...] } から { data: [...], meta: {...} } に変更。
全てのAPIクライアントの更新が必要。
```

または、type の直後に `!` を付けて Breaking Change を示す。

```
feat(api)!: レスポンス形式をJSONAPIに変更
```

`!` と `BREAKING CHANGE:` footer は併用できる。

### Issue 参照

```
fix(auth): トークンリフレッシュの競合を修正

複数タブから同時にリフレッシュリクエストが送信された場合に
トークンが無効化される問題を修正した。

Closes #123
Refs #456, #789
```

### 複数の footer

footer は複数記述できる。各 footer は `<token>: <value>` の形式で記述する。

```
fix(auth): トークンリフレッシュの競合を修正

BREAKING CHANGE: リフレッシュトークンのフォーマットが変更された
Closes #123
Reviewed-by: Alice
```

---

## 特殊なケース

### revert コミット

```
revert: feat(auth): JWT認証を実装

This reverts commit abc1234.

元のコミットで導入されたJWT認証に
セキュリティ上の問題が発見されたため一時的に取り消す。
```

### 初期コミット

```
chore: プロジェクトの初期設定

- package.json の作成
- TypeScript の設定
- ESLint / Prettier の設定
- ディレクトリ構成の作成
```

### 依存関係の更新

```
chore(deps): パッケージの依存関係を更新

- next: 14.0.0 -> 14.1.0
- react: 18.2.0 -> 18.3.0
- typescript: 5.3.0 -> 5.4.0
```

---

## コミットメッセージの検証チェックリスト

1. type は正しいか（feat, fix, refactor, docs, test, chore 等）
2. scope は適切か（変更対象を正しく表しているか）
3. subject は50文字以内か
4. subject は現在形か
5. body は必要に応じて記述されているか
6. body は72文字で折り返されているか
7. Breaking Change は正しく記述されているか
8. Issue 参照は正しい形式か
9. プロジェクトの言語（日本語/英語）に合致しているか
