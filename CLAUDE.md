# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Claude Code のスキルや各種設定を dotfiles として管理するリポジトリ。
`stow` でホームディレクトリにデプロイし、どの環境でも同じ設定を使えるようにする。

## ディレクトリ構造

```
~/dotfiles/
├── claude/                     ← stow パッケージ（Claude Code スキル）
│   └── .claude/
│       └── skills/             ← デプロイされるポータブルスキル群
├── tmux/                       ← stow パッケージ（tmux 設定）
│   ├── .tmux.conf              ← tmux 本体設定
│   └── .config/tmux/
│       └── init-session.sh     ← セッション自動構成スクリプト
├── .claude/                    ← このリポジトリ自体の開発設定
│   ├── settings.json           ← 共有設定（Agent Teams 有効化など）
│   └── settings.local.json     ← ローカル設定（パーミッション）
├── CLAUDE.md                   ← このファイル
├── deploy.sh                   ← stow デプロイスクリプト
└── docs/                       ← 仕様書・ドラフト・参考スキルサンプル
```

## スキル配置

`claude/.claude/skills/` — **ポータブルスキル（成果物）**。`stow -t ~ claude` で `~/.claude/skills/` にシンボリックリンクされ、全プロジェクトで使える。

新規スキル作成には公式プラグインの `skill-creator` を使用する。このリポジトリでは作成先を `claude/.claude/skills/` に指定すること。

## デプロイ

```bash
./deploy.sh
# または手動: stow -t ~ claude tmux
```

初回実行でシンボリックリンクが作成される。以降はリポジトリ内の変更が即反映される。

## スキル開発ワークフロー

1. このリポジトリで `claude/.claude/skills/<skill-name>/` 配下にスキルを作成・修正
2. `./deploy.sh` でデプロイ（初回のみ。以降はシンボリックリンク経由で即反映）
3. 実プロジェクトで Claude Code を起動し、スキルが意図通り動作するか検証
4. このリポジトリに戻ってフィードバックを反映

## スキル作成のルール

ポータブルスキルの制約:

- **環境非依存**: 特定のプロジェクト構造やツールに依存しない
- **自己完結**: 必要なリソースはスキルディレクトリ内に含める
- **パス参照**: スキル内のファイル参照は相対パスで記述する
