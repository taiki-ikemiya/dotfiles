# タスク類型 → 推奨チーム構成

タスクの類型に応じた推奨チーム構成の対応表。autoモードでのチーム編成の基礎として使用する。

## 対応表

| タスク類型 | 推奨構成 | リードモード | 人数 |
|---|---|---|---|
| 実装（単機能） | engineer + code-reviewer | coordinator | 2 |
| 実装（フルスタック） | backend-engineer + frontend-engineer + code-reviewer | coordinator | 3 |
| 実装（API設計含む） | backend-engineer + code-reviewer（+ frontend-engineer） | architect | 2-3 |
| 調査（技術選定） | research-analyst x2 | facilitator | 2 |
| 調査（広範囲） | research-analyst x2-3 | facilitator | 2-3 |
| ドキュメント（仕様書） | technical-writer + domain-expert | coordinator | 2 |
| ドキュメント（設計書） | technical-writer + architect的リード | architect | 2 |
| テスト設計 | test-engineer + domain-expert（+ technical-writer） | coordinator | 2-3 |
| レビュー・監査 | code-reviewer + security-auditor（+ ux-reviewer） | coordinator | 2-3 |
| セキュリティ監査 | security-auditor + code-reviewer | coordinator | 2 |
| UX改善 | ux-reviewer + frontend-engineer | coordinator | 2 |
| 混合（実装+ドキュメント） | engineer + technical-writer + code-reviewer | coordinator | 3 |
| 混合（調査+実装） | フェーズ分離を推奨 | -- | -- |

## 類型判定の基準

タスクの説明から類型を判定する際の基準:

### 実装系
- 「作って」「実装して」「追加して」「修正して」等のキーワード
- 具体的な機能やコンポーネントの言及
- ファイルパスやコード要素の言及

### 調査系
- 「調べて」「比較して」「検討して」「調査して」等のキーワード
- 技術選定やライブラリ選定の言及
- 「どちらがいいか」「メリット・デメリット」等の表現

### ドキュメント系
- 「書いて」「ドキュメント」「仕様書」「設計書」「ガイド」等のキーワード
- 既存システムの説明・整理の言及

### レビュー・監査系
- 「レビューして」「チェックして」「監査して」等のキーワード
- 品質やセキュリティの改善要求

### 混合
- 上記の複数類型にまたがる場合
- 「〜を作って、ドキュメントも書いて」等の複合的な依頼

## フェーズ分離が推奨されるケース

以下の場合はタスクをフェーズに分け、フェーズごとにチームを組み直す:

1. **調査 → 実装**: 調査結果が実装方針に影響する場合
2. **設計 → 実装**: アーキテクチャ決定が先に必要な場合
3. **実装 → ドキュメント**: 実装完了後でないとドキュメントが書けない場合

フェーズ分離する場合:
- 第1フェーズの成果物を明確にする
- 第2フェーズのチーム編成は第1フェーズ完了後に行う
- ユーザーにフェーズ分離の提案を行い、承認を得る

## domain-expert の選択

推奨構成に「domain-expert」と記載がある場合、タスクの内容に応じて以下から選択する:

| ドメイン | 選択するペルソナ |
|---|---|
| バックエンド | backend-engineer |
| フロントエンド | frontend-engineer |
| テスト | test-engineer |
| セキュリティ | security-auditor |
| UX | ux-reviewer |
