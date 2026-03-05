#!/usr/bin/env bash
# ~/.config/tmux/init-session.sh
# Ghostty起動時にtmuxセッションを自動構成するスクリプト
#
# 使い方:
#   Ghosttyの設定で command = ~/.config/tmux/init-session.sh
#   または手動で実行

set -euo pipefail

SESSION="main"

# --- OS判定でパスを切り替え ---
if [[ "$(uname)" == "Darwin" ]]; then
    # macOS
    OBSIDIAN_DIR="$HOME/Documents/Obsidian"
    DOCUMENTS_DIR="$HOME/Documents"
    DOTFILES_DIR="$HOME/.dotfiles"
    PROJECT_BASE="$HOME/projects"
else
    # Windows (WSL) / Linux
    OBSIDIAN_DIR="$HOME/documents/obsidian"
    DOCUMENTS_DIR="$HOME/documents"
    DOTFILES_DIR="$HOME/.dotfiles"
    PROJECT_BASE="$HOME/projects"
fi

# --- 既存セッションがあればattachして終了 ---
if tmux has-session -t "$SESSION" 2>/dev/null; then
    exec tmux attach-session -t "$SESSION"
fi

# ============================================================
# セッション作成 + 固定ウィンドウ
# ============================================================

# Window 0: obsidian (メモ・ナレッジベース)
tmux new-session -d -s "$SESSION" -n "obsidian" -c "$OBSIDIAN_DIR"

# Window 1: dotfiles
tmux new-window -t "$SESSION" -n "dotfiles" -c "$DOTFILES_DIR"

# Window 2: documents (Claude Codeでpptx作成など)
tmux new-window -t "$SESSION" -n "docs" -c "$DOCUMENTS_DIR"

# ============================================================
# プロジェクトウィンドウを自動生成する関数
# ============================================================
# 左: Claude Code / 右: 作業用ターミナル(neovim等)
#
# ┌──────────────────┬──────────────────┐
# │                  │                  │
# │  $ claude        │  $ nvim / shell  │
# │                  │                  │
# └──────────────────┴──────────────────┘

create_project_window() {
    local name="$1"
    local dir="$2"
    local auto_claude="${3:-false}"  # trueならClaude Codeを自動起動

    tmux new-window -t "$SESSION" -n "$name" -c "$dir"

    # 左右50:50に分割（右ペインが作業用）
    tmux split-window -t "$SESSION:$name" -h -c "$dir"

    # 左ペイン（ペイン0）でClaude Code起動
    if [[ "$auto_claude" == "true" ]]; then
        tmux send-keys -t "$SESSION:$name.0" "claude" Enter
    else
        # プロンプトだけ表示（手動起動用）
        tmux send-keys -t "$SESSION:$name.0" "# claude  ← 準備できたらEnter" ""
    fi

    # 右ペイン（ペイン1）にフォーカス
    tmux select-pane -t "$SESSION:$name.1"
}

# --- プロジェクト登録 ---
# ここに自分のプロジェクトを追加していく
# create_project_window "ウィンドウ名" "ディレクトリ" "claude自動起動(true/false)"

create_project_window "mitococa"  "$PROJECT_BASE/mitococa-edge"  false
create_project_window "vlm-retail" "$PROJECT_BASE/vlm-retail"     false
# create_project_window "fabric"    "$PROJECT_BASE/fabric-defect"  false
# create_project_window "sandbox"   "$PROJECT_BASE/sandbox"        true

# ============================================================
# 初期表示: 最初のウィンドウを選択してattach
# ============================================================
tmux select-window -t "$SESSION:0"
exec tmux attach-session -t "$SESSION"
