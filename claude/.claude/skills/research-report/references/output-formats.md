# 出力形式ガイドライン

Markdown出力とPPTX出力の切り替え基準、および pptx-builder への引き渡しデータ形式。

---

## 出力形式の切り替え基準

### Markdown出力を選択する場合

- 社内のエンジニア向け共有
- ドキュメントとしてリポジトリに蓄積する
- 技術的な詳細やコード例を多く含む
- 継続的に更新する予定がある
- Git管理したい

### PPTX出力を選択する場合

- 報告会やプレゼンテーションで使用する
- 対外向けの報告資料として提出する
- 経営層やマネージャーに説明する
- 視覚的なインパクトが必要
- 印刷して配布する

### 判定フローチャート

```
ユーザーの依頼を確認
├─ 「スライド」「プレゼン」「PPTX」「発表」と明示 → PPTX
├─ 「レポート」「ドキュメント」「Markdown」と明示 → Markdown
├─ 対象読者が経営層・外部顧客 → PPTX を提案
├─ 対象読者がエンジニア・社内チーム → Markdown を提案
└─ 不明な場合 → ユーザーに確認する
```

---

## Markdown出力仕様

### ファイル形式

- 拡張子: `.md`
- 文字コード: UTF-8
- 改行コード: LF

### 記法ルール

- 見出しは `#` から `####` までを使用する（`#####` 以降は使わない）
- 表は GitHub Flavored Markdown (GFM) 形式で記述する
- コードブロックは言語指定付きフェンスを使用する
- チェックリストは `- [ ]` / `- [x]` を使用する
- リンクは `[テキスト](URL)` 形式で記述する

### 出力先

ユーザーが指定した場所に出力する。指定がない場合はカレントディレクトリに出力する。

ファイル名の規則:
```
{YYYY-MM-DD}_{テーマ概要}_report.md
```

例: `2026-02-28_fastapi-vs-django_report.md`

---

## PPTX出力仕様

### pptx-builder への引き渡し

PPTX出力が必要な場合は、pptx-builder スキルに構造化データを引き渡す。

### 引き渡しデータ形式

以下のJSON構造でデータを組み立て、pptx-builder に渡す。

```json
{
  "metadata": {
    "title": "レポートタイトル",
    "subtitle": "サブタイトル（任意）",
    "author": "作成者",
    "date": "YYYY-MM-DD",
    "type": "internal | external"
  },
  "slides": [
    {
      "type": "title",
      "title": "メインタイトル",
      "subtitle": "サブタイトル"
    },
    {
      "type": "summary",
      "title": "エグゼクティブサマリー",
      "bullets": [
        "結論1",
        "結論2",
        "結論3"
      ]
    },
    {
      "type": "content",
      "title": "セクションタイトル",
      "body": "本文テキスト",
      "bullets": ["箇条書き1", "箇条書き2"],
      "notes": "スピーカーノート"
    },
    {
      "type": "comparison",
      "title": "比較・分析",
      "table": {
        "headers": ["項目", "A", "B"],
        "rows": [
          ["パフォーマンス", "◎", "○"],
          ["学習コスト", "○", "△"]
        ]
      }
    },
    {
      "type": "action",
      "title": "Next Steps",
      "items": [
        {"task": "タスク内容", "owner": "担当者", "deadline": "期限"},
        {"task": "タスク内容", "owner": "担当者", "deadline": "期限"}
      ]
    }
  ]
}
```

### スライドタイプ一覧

| type | 用途 | 必須フィールド |
|---|---|---|
| title | 表紙 | title, subtitle |
| summary | エグゼクティブサマリー | title, bullets |
| content | 本文スライド | title, body または bullets |
| comparison | 比較表 | title, table |
| action | Next Steps | title, items |
| section | セクション区切り | title |

### Markdownからスライドへの変換ルール

| Markdown要素 | スライド変換 |
|---|---|
| `# タイトル` | title スライド |
| `## エグゼクティブサマリー` | summary スライド |
| `## セクション` | section スライド + content スライド |
| `### サブセクション` | content スライド |
| 比較表 | comparison スライド |
| `## Next Steps` | action スライド |
| 箇条書き | bullets フィールド |
| コードブロック | 原則省略（必要ならノートに記載） |

---

## 連携手順

### Markdown → PPTX 変換の流れ

1. research-report でMarkdownドラフトを作成する
2. ドラフトを上記の引き渡しデータ形式に変換する
3. pptx-builder スキルを呼び出し、データを渡す
4. pptx-builder がPPTXファイルを生成する

### 注意事項

- コードブロックはスライドには含めない（読みにくいため）
- 長文の本文は箇条書きに変換する
- 1スライドあたり箇条書きは5項目以内にする
- 表は行数が多い場合、複数スライドに分割する
