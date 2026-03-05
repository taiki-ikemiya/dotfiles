---
name: pptx-builder
description: python-pptxでPowerPointスライドを生成する。プレゼン、スライド、発表資料、pptx、パワポ、PowerPointに言及された場合は必ずこのスキルを使うこと。research-reportからのPPTX出力時にも使用する。
---

# pptx-builder スキル

python-pptx を用いて PPTX ファイルを生成する汎用スキル。

---

## 設計方針

- **パターン駆動**: 3つのデザインパターンから用途に応じて選択する
- **構造化入力**: JSON 形式でスライドデータを受け取る
- **ブランド統一**: 共通カラーパレットをパターンごとの配色比率で適用する

---

## デザインパターン

| パターン | 用途 | 印象 | デフォルト |
|---|---|---|---|
| `clean_pro` | 個人作業・チーム報告・技術文書 | プロフェッショナル・整然・信頼 | **はい** |
| `soft_business` | 提案資料・サービス紹介・HP/LP | やさしさとビジネス品格の両立 | |
| `warm_formal` | クライアント提案・SNS・ブランド訴求 | 温かみとフォーマルさの融合 | |

### パターン選択の指針

- **個人作業やチーム内報告** → `clean_pro`（デフォルト）
- **対外向け提案・一般向け資料** → `soft_business` または `warm_formal`
- ユーザーが指定しない場合は `clean_pro` を使用する

### パターンごとの特徴

| 属性 | soft_business | clean_pro | warm_formal |
|---|---|---|---|
| 角丸 | やや丸い | シャープ | やや丸い / ピル型CTA |
| カード背景 | 白 | 白 | ピンクベージュ |
| カード枠線 | あり | あり | なし |
| ヘッダー | 白背景 + 下線 | bg背景 + 上部primaryライン | primary塗り + 白文字 |
| 見出し色 | primary（テラコッタ） | text（ダークブラウン） | primary（テラコッタ） |
| テーブルヘッダー | warm背景 | primary背景 + 白文字 | primary背景 + 白文字 |

---

## 生成スクリプト

`scripts/generate_pptx.py` を使用して PPTX を生成する。

### 実行方法

```bash
python scripts/generate_pptx.py --input <入力JSON> --output <出力パス> [--pattern <パターン名>]
```

### 引数

| 引数 | 必須 | 説明 |
|---|---|---|
| `--input` / `-i` | はい | 入力JSONファイルのパス |
| `--output` / `-o` | はい | 出力PPTXファイルのパス |
| `--pattern` / `-p` | いいえ | デザインパターン名（デフォルト: `clean_pro`） |

`--pattern` を指定した場合、JSON内の `pattern` フィールドより優先する。

---

## 入力データ構造

JSON形式でスライドの構成を定義する。

```json
{
  "pattern": "clean_pro",
  "title": "プレゼンタイトル",
  "subtitle": "サブタイトル",
  "author": "作成者名",
  "date": "2026-02-28",
  "slides": [
    {
      "layout": "content_text",
      "title": "スライドタイトル",
      "content": ["箇条書き1", "箇条書き2"]
    },
    {
      "layout": "content_cards",
      "title": "サービス紹介",
      "cards": [
        {"label": "機能A", "description": "説明文"},
        {"label": "機能B", "description": "説明文"},
        {"label": "機能C", "description": "説明文"}
      ]
    }
  ]
}
```

### トップレベルフィールド

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `pattern` | string | いいえ | デザインパターン名（デフォルト: `clean_pro`） |
| `title` | string | はい | プレゼンテーションのタイトル |
| `subtitle` | string | いいえ | サブタイトル |
| `author` | string | いいえ | 作成者名（タイトルスライドに表示） |
| `date` | string | いいえ | 日付（タイトルスライドに表示） |
| `slides` | array | はい | スライドの配列 |

### スライドオブジェクト共通フィールド

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `layout` | string | はい | レイアウト種別 |
| `title` | string | レイアウト依存 | スライドタイトル |

レイアウトごとの追加フィールドは `references/slide-layouts.md` を参照すること。

---

## 利用可能なレイアウト

| レイアウト | 説明 |
|---|---|
| `title_slide` | タイトルスライド（表紙） |
| `toc` | 目次スライド |
| `section_divider` | セクション区切りスライド |
| `content_text` | テキスト・箇条書きコンテンツ |
| `content_cards` | カード型コンテンツ（2〜4枚） |
| `content_data` | KPI・数値ハイライト |
| `content_table` | テーブル・比較表 |
| `closing` | クロージングスライド |
| `two_column` | 2カラム比較レイアウト |
| `blank` | 白紙スライド |

後方互換: `title_content` は `content_text` と同じ動作をする。

各レイアウトの詳細は `references/slide-layouts.md` を参照すること。

---

## ワークフロー

以下の手順で PPTX を生成する。

1. ユーザーの要件からスライド構成を設計する
2. **用途に応じてデザインパターンを選択する**（デフォルト: `clean_pro`）
3. 入力データを JSON 形式で構造化する
4. JSON ファイルを一時ファイルとして書き出す
5. `scripts/generate_pptx.py` を実行して PPTX を生成する
6. 出力先: `~/Documents/<ファイル名>.pptx`（ユーザーの指示があればそちらに従う）
7. 生成結果をユーザーに報告する

### 実行例

```bash
python scripts/generate_pptx.py --input /tmp/slides.json --output ~/Documents/presentation.pptx --pattern clean_pro
```

---

## カラーパレット

全パターン共通の6色 + 補助色を使用する。

| トークン | HEX | 用途 |
|---|---|---|
| `primary` | `#C07A5A` | テラコッタブラウン：見出し・CTA・キービジュアル |
| `secondary` | `#8FBA78` | ナチュラルグリーン：図表・アイコン・区切り |
| `accent` | `#6B8FA4` | スレートブルー：技術・信頼要素（控えめ） |
| `warm` | `#F2DED8` | ピンクベージュ：カード背景・温かみ |
| `text` | `#3B3533` | ダークブラウン：本文テキスト |
| `bg` | `#F9F8F7` | ウォームグレー：スライド背景 |

### 補助色

| トークン | HEX | 用途 |
|---|---|---|
| `white` | `#FFFFFF` | カード背景・テーブル背景 |
| `border` | `#E4DFDC` | 枠線・区切り線 |
| `subtext` | `#9A8E8B` | 補足テキスト・キャプション |

### フォント

- プライマリ: Noto Sans JP
- フォールバック: Segoe UI

---

## 連携

### research-report との連携

research-report スキルが PPTX 出力を要求された場合、以下の手順で連携する。

1. research-report がレポート内容を構造化する
2. 構造化データを pptx-builder の入力JSON形式に変換する
3. pptx-builder の `scripts/generate_pptx.py` を実行して PPTX を生成する

### 入力データの変換指針

- レポートの表紙 → `title_slide`
- 目次 → `toc`
- セクション区切り → `section_divider`
- エグゼクティブサマリー → `content_text`
- 特徴・比較一覧 → `content_cards`
- KPI・数値データ → `content_data`
- 比較表 → `content_table`
- 結論・まとめ → `closing`

---

## エラーハンドリング

- python-pptx がインストールされていない場合は `pip install python-pptx` を実行する
- 不明なパターン名が指定された場合は `clean_pro` にフォールバックする
- 入力JSONのバリデーションエラー時は具体的なエラーメッセージを返す
- 出力ディレクトリが存在しない場合は自動作成する

---

## 後方互換

- `--template` オプションは `--pattern` のエイリアスとして引き続き動作する
- JSON の `template` フィールドも `pattern` のエイリアスとして動作する
- レガシーテンプレート名は自動変換される: `minimal` → `clean_pro`、`internal` → `clean_pro`、`external` → `soft_business`
- `title_content` レイアウトは `content_text` と同じ動作をする

---

## 制約事項

- 画像の埋め込みは現時点では未対応（将来拡張予定）
- グラフ・チャートの自動生成は未対応（画像として事前生成すること）
- アニメーション設定は未対応
- スライドマスターの編集は未対応
