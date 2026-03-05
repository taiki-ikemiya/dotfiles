#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STOW_PACKAGES=(claude tmux ghostty)

cd "$SCRIPT_DIR"

# stow がインストールされているか確認
if ! command -v stow &>/dev/null; then
  echo "Error: stow がインストールされていません。"
  echo "  Ubuntu/Debian: sudo apt install stow"
  echo "  macOS: brew install stow"
  exit 1
fi

# デプロイ（冪等: 既存のシンボリックリンクがあっても安全に再実行可能）
for pkg in "${STOW_PACKAGES[@]}"; do
  stow -v -t "$HOME" --restow "$pkg"
done

echo "デプロイ完了: 以下のパッケージをデプロイしました: ${STOW_PACKAGES[*]}"

# --- ccstatusline インストール ---
if command -v npm &>/dev/null; then
  if npm list -g ccstatusline &>/dev/null; then
    echo "ccstatusline 既存"
  else
    echo "ccstatusline をインストール"
    npm install -g ccstatusline@latest
  fi
else
  echo "Warning: npm が見つかりません。ccstatusline のインストールをスキップします。"
fi

# --- フォントインストール (GeistMono Nerd Font) ---
if [[ "$(uname)" == "Darwin" ]]; then
  if command -v brew &>/dev/null; then
    if brew list --cask font-geist-mono-nerd-font &>/dev/null; then
      echo "フォント既存: font-geist-mono-nerd-font"
    else
      echo "フォントをインストール: font-geist-mono-nerd-font"
      brew install --cask font-geist-mono-nerd-font
    fi
  fi
elif [[ "$(uname)" == "Linux" ]]; then
  FONT_DIR="$HOME/.local/share/fonts/GeistMonoNerdFont"
  if [[ -d "$FONT_DIR" ]]; then
    echo "フォント既存: GeistMono Nerd Font"
  else
    echo "フォントをインストール: GeistMono Nerd Font"
    FONT_URL="https://github.com/ryanoasis/nerd-fonts/releases/latest/download/GeistMono.zip"
    TMP_ZIP="$(mktemp /tmp/GeistMono-XXXXXX.zip)"
    curl -fsSL -o "$TMP_ZIP" "$FONT_URL"
    mkdir -p "$FONT_DIR"
    unzip -o "$TMP_ZIP" -d "$FONT_DIR"
    rm -f "$TMP_ZIP"
    fc-cache -f "$FONT_DIR"
  fi
fi
