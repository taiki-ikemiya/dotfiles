---
name: team-up
description: Agent Teamsのチーム編成・起動を行う。タスクに最適なメンバーを選定しチームを起動する。「チームを組んで」「みんなでやって」「並行作業で」「チーム編成して」「メンバーを集めて」等の依頼では必ずこのスキルを使うこと。
---

# team-up: チーム編成・起動スキル

タスクに最適なAgent Teamsチームを編成し起動する。蓄積されたペルソナ定義と編成原則に基づき、効果的なチーム構成を実現する。

## 2つのモード

### auto モード
タスクだけ伝えると、最適なチーム編成を提案し、承認後に起動する。

### manual モード
メンバーを直接指定する、または自然言語で要望を伝える。

## コマンド

```
/team-up auto <タスク説明>
/team-up auto --lead <リードモード> <タスク説明>
/team-up manual --members <メンバー名,...> <タスク説明>
/team-up manual <自然言語での要望>
/team-up roster                    # 全メンバー一覧
/team-up roster <メンバー名>       # 特定メンバー詳細
/team-up leads                     # リードモード一覧
```

### 使用例

```
/team-up auto プロジェクトXのシステムテスト設計書を作成して
/team-up auto --lead architect 新機能のAPI設計
/team-up manual --members backend-engineer,test-engineer ユーザー認証APIのテスト
/team-up roster
/team-up roster research-analyst
/team-up leads
```

## auto モードのフロー

### 1. タスク分析

以下の観点でタスクを分析する:

- **類型判定**: 実装 / 調査 / ドキュメント / レビュー / 混合
- **専門性特定**: 必要な技術領域・ドメイン知識
- **並行分割点**: 独立して進められる作業の境界
- **ファイル競合評価**: 複数メンバーが同一ファイルを編集するリスク

### 2. 編成原則の適用

`references/composition-principles.md` に定義された7原則を適用する:

- **P1: 最小有効チーム** -- 2-4人が基本。5人以上は例外的な場合のみ
- **P2: ファイル所有権の分離** -- 各メンバーの担当ファイルを明確に分ける
- **P3: 作る人と見る人を分ける** -- 実装者とレビュー者を別にする

詳細は `references/composition-principles.md` を参照。

### 3. Team Proposal 提示

分析結果をもとに以下の形式で提案する:

```
📋 Team Proposal

Task: システムテスト設計書の作成
Type: ドキュメント + テスト設計
Lead: coordinator（調整型）

👥 Members (3):
 1. test-engineer (リード) → テスト設計・ケース作成
 2. backend-engineer → 実装仕様確認・技術制約共有
 3. technical-writer → ドキュメント構成・品質レビュー

⚠️ 注意: テスト設計書テンプレートがあれば事前共有推奨

[承認] [メンバー変更] [やり直し]
```

提案に含める情報:
- タスク要約と類型
- 選択したリードモードとその理由
- メンバー一覧（役割と担当内容）
- 注意事項・前提条件
- ユーザーの選択肢

### 4. 承認後の起動

ユーザーが承認したら:

1. `TeamCreate` でチームを作成する
2. 各メンバーを `Task` でspawnする
3. spawn時に以下を含める:
   - ペルソナ定義（roster/<name>.md の Spawn Prompt Template）
   - タスクの説明と担当範囲
   - 他メンバーとの連携ポイント
   - ファイル所有権の明示

## リードモード

リードはspawnせず、自分自身（team-up実行者）の指揮スタイルとして適用する。

### 自動選択ルール

| タスク特性 | 選択されるリード |
|---|---|
| 実装中心・明確なゴール | coordinator |
| 設計判断を含む | architect |
| 調査・比較・意思決定 | facilitator |
| `--lead` 指定あり | 指定に従う |

### 利用可能なリードモード

`lead-modes/_index.yaml` を参照。各モードの詳細は `lead-modes/<name>.md` にある。

- **coordinator**: 作業分配と進捗管理に集中。自分では実装しない（デフォルト）
- **architect**: 設計判断を主導。技術方針を決めてから委譲
- **facilitator**: メンバー間の議論を促進。仮説の対立を活かす

## ペルソナ一覧

`roster/_index.yaml` を参照。各ペルソナの詳細は `roster/<name>.md` にある。

| ペルソナ | 概要 |
|---|---|
| backend-engineer | バックエンド実装。API設計、DB操作、パフォーマンス最適化 |
| frontend-engineer | フロントエンド実装。UI構築、状態管理、レスポンシブ対応 |
| code-reviewer | コードレビュー。設計妥当性、バグ検出、改善提案 |
| technical-writer | ドキュメント作成。仕様書、設計書、ユーザーガイド |
| research-analyst | 技術調査・分析。ライブラリ比較、技術動向、PoC設計 |
| test-engineer | テスト設計・実装。テスト戦略、ケース設計、自動化 |
| security-auditor | セキュリティ監査。脆弱性チェック、権限設計レビュー |
| ux-reviewer | UXレビュー。ユーザビリティ評価、アクセシビリティチェック |

## manual モード

### --members 指定

```
/team-up manual --members backend-engineer,test-engineer ユーザー認証APIのテスト
```

指定されたメンバーをそのまま採用する。ただし編成原則に明らかに反する場合は警告を出す。

### 自然言語指定

```
/team-up manual セキュリティに詳しい人とバックエンドの人でログイン機能をレビューして
```

要望から適切なメンバーをマッチングし、Team Proposalとして提示する。

## roster / leads コマンド

### roster（一覧）

`/team-up roster` で全ペルソナの一覧を表形式で表示する。

### roster（詳細）

`/team-up roster <メンバー名>` で該当メンバーの詳細情報を表示する。`roster/<name>.md` の内容をもとに、役割・得意領域・連携先を提示する。

### leads

`/team-up leads` で全リードモードの一覧と説明を表示する。

## タスク類型と推奨構成

基本的な対応は `references/task-team-mapping.md` を参照。

| タスク類型 | 推奨構成 |
|---|---|
| 実装（単機能） | engineer + reviewer |
| 実装（フルスタック） | backend + frontend + reviewer |
| 調査 | research-analyst x2-3 |
| ドキュメント | writer + domain-expert |
| レビュー・監査 | reviewer x2-3 |
| 混合 | engineer + writer + reviewer |

## アンチパターン

以下の編成は避ける。詳細は `references/anti-patterns.md` を参照。

- 全員実装者でレビューなし
- ファイル境界が曖昧
- リード不在の大チーム
- 過剰な人数
- コンテキスト不足のspawn

## spawn時のプロンプト構成

各メンバーをspawnする際、以下の情報をプロンプトに含める:

1. **ペルソナ定義**: `roster/<name>.md` の Spawn Prompt Template
2. **タスク説明**: 全体タスクと個別の担当範囲
3. **ファイル所有権**: そのメンバーが編集してよいファイル
4. **連携情報**: 他メンバーとの受け渡しポイント
5. **完了条件**: 何をもって完了とするか

## 参照ファイル

- `references/composition-principles.md` -- 編成原則の詳細
- `references/anti-patterns.md` -- 避けるべきパターン
- `references/task-team-mapping.md` -- タスク類型と推奨構成
- `lead-modes/_index.yaml` -- リードモード一覧
- `roster/_index.yaml` -- ペルソナ一覧
