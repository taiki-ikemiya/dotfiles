---
name: chart-generator
description: >
  matplotlib を使って PNG チャート画像を生成するスキル。
  学習曲線（loss/accuracy の推移）、混同行列（ヒートマップ）、棒グラフ、折れ線グラフなど、
  ML 実験の可視化に特化した図表を作成する。
  「グラフを作って」「学習曲線を描いて」「混同行列を可視化」「精度の推移をプロット」
  「図表を作成」「チャートを生成」「実験結果を可視化」等の依頼では必ずこのスキルを使うこと。
  research-report スキルや pptx-builder スキルからのチャート生成依頼でも使用する。
  レポートやスライドに図表を含めたい場合、まずこのスキルでPNG画像を生成してから
  他スキルに渡す流れになる。
---

# chart-generator スキル

matplotlib を使い、JSON データから美しいチャート PNG 画像を生成する。
ML/DL 実験の可視化を主な用途とするが、汎用的なグラフ作成にも対応する。

## 使い方の流れ

1. ユーザーの要望やデータからチャート定義 JSON を組み立てる
2. `scripts/generate_chart.py` に JSON を渡して PNG を生成する
3. 生成された PNG をユーザーに提示する（または他スキルに渡す）

## 対応チャート種類

| chart_type        | 用途                               | 典型的な使い方                     |
|-------------------|------------------------------------|------------------------------------|
| `learning_curve`  | 学習曲線                           | train/val の loss・accuracy 推移   |
| `confusion_matrix`| 混同行列                           | 分類結果のヒートマップ表示         |
| `bar`             | 棒グラフ                           | 実験比較、カテゴリ別の精度比較     |
| `line`            | 折れ線グラフ                       | 精度推移、メトリクスのトレンド     |
| `grouped_bar`     | グループ化棒グラフ                 | 複数条件の比較                     |
| `multi_line`      | 複数折れ線グラフ                   | 複数実験の同一指標での比較         |

## JSON 入力フォーマット

チャート定義は以下の JSON 構造で渡す。`scripts/generate_chart.py` が受け取る。

### 共通フィールド

```json
{
  "chart_type": "learning_curve",
  "title": "チャートタイトル",
  "output_path": "output/chart.png",
  "figsize": [10, 6],
  "dpi": 150,
  "style": "default",
  "lang": "ja"
}
```

- `chart_type` (必須): チャートの種類
- `title` (必須): チャートのタイトル
- `output_path` (必須): 出力 PNG のパス
- `figsize`: 図のサイズ [幅, 高さ] インチ（デフォルト: [10, 6]）
- `dpi`: 解像度（デフォルト: 150）
- `style`: 配色スタイル。`"default"` / `"presentation"`（デフォルト: `"default"`）
  - `default`: 論文・レポート向け、落ち着いた配色
  - `presentation`: スライド向け、コントラスト高めの配色
- `lang`: ラベルの言語。`"ja"` / `"en"`（デフォルト: `"ja"`）

### chart_type 別のフィールド

#### `learning_curve` — 学習曲線

```json
{
  "chart_type": "learning_curve",
  "title": "学習曲線",
  "output_path": "output/learning_curve.png",
  "x_label": "Epoch",
  "y_label": "Loss",
  "series": [
    {
      "label": "Train Loss",
      "values": [0.9, 0.7, 0.5, 0.35, 0.25]
    },
    {
      "label": "Val Loss",
      "values": [0.95, 0.8, 0.65, 0.55, 0.5]
    }
  ],
  "x_values": [1, 2, 3, 4, 5],
  "best_epoch": 4,
  "secondary_y": {
    "y_label": "Accuracy",
    "series": [
      {
        "label": "Val Accuracy",
        "values": [0.6, 0.7, 0.78, 0.82, 0.80]
      }
    ]
  }
}
```

- `series` (必須): 各系列。`label` と `values`（数値リスト）を持つ
- `x_values`: X 軸の値（省略時は 1 始まりの連番）
- `x_label` / `y_label`: 軸ラベル
- `best_epoch`: 最良エポックに縦線マーカーを表示（省略可）
- `secondary_y`: 第2Y軸に表示する系列（loss と accuracy を1つのグラフに描く場合）

#### `confusion_matrix` — 混同行列

```json
{
  "chart_type": "confusion_matrix",
  "title": "混同行列",
  "output_path": "output/confusion_matrix.png",
  "matrix": [[85, 5], [10, 100]],
  "labels": ["OK", "NG"],
  "normalize": false,
  "show_values": true,
  "cmap": "Blues"
}
```

- `matrix` (必須): 2次元配列（実数 or 整数）
- `labels` (必須): クラスラベル
- `normalize`: 正規化表示するか（デフォルト: false）
- `show_values`: セルに数値を表示するか（デフォルト: true）
- `cmap`: カラーマップ名（デフォルト: `"Blues"`）

#### `bar` — 棒グラフ

```json
{
  "chart_type": "bar",
  "title": "実験別 Accuracy",
  "output_path": "output/bar.png",
  "x_label": "実験",
  "y_label": "Accuracy",
  "categories": ["exp001", "exp002", "exp003"],
  "values": [0.85, 0.90, 0.88],
  "error_bars": [0.02, 0.01, 0.03],
  "highlight": [1],
  "y_range": [0.8, 0.95],
  "horizontal": false,
  "show_values": true
}
```

- `categories` (必須): カテゴリラベル
- `values` (必須): 値
- `error_bars`: エラーバー（省略可）
- `highlight`: ハイライトするバーのインデックスリスト
- `y_range`: Y軸の範囲 [min, max]（省略時は自動）
- `horizontal`: 横棒グラフにするか（デフォルト: false）
- `show_values`: バー上に値を表示するか（デフォルト: true）

#### `grouped_bar` — グループ化棒グラフ

```json
{
  "chart_type": "grouped_bar",
  "title": "バックボーン別精度比較",
  "output_path": "output/grouped_bar.png",
  "x_label": "バックボーン",
  "y_label": "Score",
  "categories": ["ResNet50", "EfficientNet-B0", "ConvNeXt-T"],
  "groups": [
    {"label": "Accuracy", "values": [0.85, 0.90, 0.92]},
    {"label": "F1-Score", "values": [0.83, 0.88, 0.91]}
  ],
  "y_range": [0.8, 0.95],
  "show_values": true
}
```

- `categories` (必須): X 軸のカテゴリ
- `groups` (必須): グループごとの `label` と `values`

#### `line` — 折れ線グラフ

```json
{
  "chart_type": "line",
  "title": "学習率スケジュール",
  "output_path": "output/line.png",
  "x_label": "Step",
  "y_label": "Learning Rate",
  "x_values": [0, 100, 200, 300, 400, 500],
  "values": [0.001, 0.01, 0.008, 0.005, 0.002, 0.0005]
}
```

- `values` (必須): Y 軸の値
- `x_values`: X 軸の値（省略時は連番）

#### `multi_line` — 複数折れ線

```json
{
  "chart_type": "multi_line",
  "title": "実験別 Validation Accuracy 推移",
  "output_path": "output/multi_line.png",
  "x_label": "Epoch",
  "y_label": "Val Accuracy",
  "x_values": [1, 2, 3, 4, 5],
  "series": [
    {"label": "exp001", "values": [0.6, 0.7, 0.75, 0.80, 0.82]},
    {"label": "exp002", "values": [0.65, 0.72, 0.80, 0.85, 0.87]},
    {"label": "exp003", "values": [0.60, 0.68, 0.73, 0.78, 0.80]}
  ]
}
```

- `series` (必須): 各系列。`label` と `values` を持つ

## 実行方法

```bash
python ~/.claude/skills/chart-generator/scripts/generate_chart.py \
  --input chart_def.json \
  --output output/chart.png
```

- `--input`: チャート定義 JSON ファイルのパス
- `--output`: 出力 PNG パス（JSON 内の `output_path` より優先）

複数チャートを一括生成する場合は、JSON 配列で渡す：

```bash
python ~/.claude/skills/chart-generator/scripts/generate_chart.py \
  --input charts.json
```

```json
[
  {"chart_type": "learning_curve", "title": "...", "output_path": "chart1.png", ...},
  {"chart_type": "confusion_matrix", "title": "...", "output_path": "chart2.png", ...}
]
```

## 他スキルとの連携

### research-report との連携

レポートに図表を含めたい場合：

1. レポート作成中にチャートデータを特定する
2. このスキルで PNG を生成する
3. Markdown 内に `![タイトル](path/to/chart.png)` で挿入する

### pptx-builder との連携

スライドにチャートを含めたい場合：

1. このスキルで PNG を生成する（`style: "presentation"` 推奨）
2. pptx-builder の `content_image` レイアウト（または blank スライドへの画像配置）で埋め込む

> pptx-builder 側に画像挿入レイアウトが未実装の場合は、
> `python-pptx` で直接画像を挿入するコードを書いて対応する。

## デザイン方針

### default スタイル（レポート向け）
- 落ち着いたカラーパレット：`#4C72B0`, `#DD8452`, `#55A868`, `#C44E52`, `#8172B3`
- 白背景、控えめなグリッド線
- フォント: 読みやすさ優先

### presentation スタイル（スライド向け）
- 高コントラストのカラーパレット：`#C07A5A`, `#8FBA78`, `#6B8FA4`, `#D4A84B`, `#9B6B9E`
  - pptx-builder のカラーパレットと調和する配色
- 大きめのフォントサイズ、太い線
- 見やすさ優先

### 日本語対応
- `lang: "ja"` の場合、日本語フォント（IPAexGothic 等）を自動設定する
- フォントが見つからない場合はフォールバック処理を行う
