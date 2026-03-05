#!/usr/bin/env python3
"""チャート生成スクリプト — JSON 定義から matplotlib で PNG チャートを生成する."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")

# ---------------------------------------------------------------------------
# カラーパレット
# ---------------------------------------------------------------------------

PALETTES: dict[str, list[str]] = {
    "default": ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860", "#DA8BC3", "#8C8C8C"],
    "presentation": ["#C07A5A", "#8FBA78", "#6B8FA4", "#D4A84B", "#9B6B9E", "#E07B7B", "#5BA58B", "#B8860B"],
}

HIGHLIGHT_COLOR = "#E74C3C"

# ---------------------------------------------------------------------------
# 日本語フォント設定
# ---------------------------------------------------------------------------


def _setup_japanese_font() -> None:
    """日本語フォントを設定する。利用可能なフォントを自動検出してフォールバック。"""
    import matplotlib.font_manager as fm

    candidates = [
        "IPAexGothic",
        "IPAGothic",
        "Noto Sans CJK JP",
        "Noto Sans JP",
        "Yu Gothic",
        "Hiragino Sans",
        "MS Gothic",
        "TakaoPGothic",
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            return
    # フォールバック: sans-serif のまま
    print("[chart-generator] Warning: 日本語フォントが見つかりません。文字化けの可能性があります。", file=sys.stderr)


# ---------------------------------------------------------------------------
# スタイル設定
# ---------------------------------------------------------------------------


def _apply_style(style: str, lang: str) -> list[str]:
    """matplotlib のスタイルを設定し、カラーパレットを返す."""
    palette = PALETTES.get(style, PALETTES["default"])

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.grid": True,
            "grid.alpha": 0.3,
            "grid.linestyle": "--",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    if style == "presentation":
        plt.rcParams.update(
            {
                "font.size": 14,
                "axes.titlesize": 18,
                "axes.labelsize": 14,
                "xtick.labelsize": 12,
                "ytick.labelsize": 12,
                "legend.fontsize": 12,
                "lines.linewidth": 2.5,
                "lines.markersize": 8,
            }
        )
    else:
        plt.rcParams.update(
            {
                "font.size": 11,
                "axes.titlesize": 14,
                "axes.labelsize": 12,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
                "legend.fontsize": 10,
                "lines.linewidth": 2.0,
                "lines.markersize": 6,
            }
        )

    if lang == "ja":
        _setup_japanese_font()

    return palette


# ---------------------------------------------------------------------------
# チャート描画関数
# ---------------------------------------------------------------------------


def _draw_learning_curve(ax: plt.Axes, spec: dict[str, Any], palette: list[str]) -> None:
    """学習曲線を描画する."""
    series = spec["series"]
    x_values = spec.get("x_values") or list(range(1, len(series[0]["values"]) + 1))

    for i, s in enumerate(series):
        color = palette[i % len(palette)]
        linestyle = "-" if i % 2 == 0 else "--"
        ax.plot(x_values, s["values"], label=s["label"], color=color, linestyle=linestyle, marker="o", markersize=4)

    # 第2Y軸
    secondary = spec.get("secondary_y")
    if secondary:
        ax2 = ax.twinx()
        ax2.set_ylabel(secondary.get("y_label", ""))
        ax2.spines["top"].set_visible(False)
        offset = len(series)
        for j, s in enumerate(secondary["series"]):
            color = palette[(offset + j) % len(palette)]
            ax2.plot(x_values, s["values"], label=s["label"], color=color, linestyle=":", marker="s", markersize=4)
        ax2.legend(loc="center right")

    # ベストエポック
    best = spec.get("best_epoch")
    if best is not None:
        ax.axvline(x=best, color="#888888", linestyle=":", alpha=0.7, label=f"Best epoch = {best}")

    ax.set_xlabel(spec.get("x_label", "Epoch"))
    ax.set_ylabel(spec.get("y_label", ""))
    ax.legend(loc="best")


def _draw_confusion_matrix(ax: plt.Axes, spec: dict[str, Any], palette: list[str]) -> None:
    """混同行列をヒートマップで描画する."""
    matrix = np.array(spec["matrix"], dtype=float)
    labels = spec["labels"]
    normalize = spec.get("normalize", False)
    show_values = spec.get("show_values", True)
    cmap = spec.get("cmap", "Blues")

    if normalize:
        row_sums = matrix.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # ゼロ除算防止
        matrix = matrix / row_sums

    im = ax.imshow(matrix, interpolation="nearest", cmap=cmap, aspect="equal")
    ax.figure.colorbar(im, ax=ax, shrink=0.8)

    tick_marks = np.arange(len(labels))
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(labels)
    ax.set_yticks(tick_marks)
    ax.set_yticklabels(labels)
    ax.set_xlabel(spec.get("x_label", "Predicted"))
    ax.set_ylabel(spec.get("y_label", "Actual"))

    if show_values:
        thresh = matrix.max() / 2.0
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                val = matrix[i, j]
                text = f"{val:.2f}" if normalize else f"{int(val)}"
                ax.text(j, i, text, ha="center", va="center", color="white" if val > thresh else "black", fontsize=12)

    # グリッド不要
    ax.grid(False)


def _draw_bar(ax: plt.Axes, spec: dict[str, Any], palette: list[str]) -> None:
    """棒グラフを描画する."""
    categories = spec["categories"]
    values = spec["values"]
    horizontal = spec.get("horizontal", False)
    show_values = spec.get("show_values", True)
    highlight = set(spec.get("highlight", []))
    error_bars = spec.get("error_bars")

    colors = [HIGHLIGHT_COLOR if i in highlight else palette[0] for i in range(len(categories))]
    x = np.arange(len(categories))

    if horizontal:
        bars = ax.barh(x, values, color=colors, xerr=error_bars, capsize=4, edgecolor="white", height=0.6)
        ax.set_yticks(x)
        ax.set_yticklabels(categories)
        ax.set_xlabel(spec.get("y_label", ""))
        ax.set_ylabel(spec.get("x_label", ""))
        if show_values:
            for bar, v in zip(bars, values):
                ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2, f"{v:.3f}", va="center")
    else:
        bars = ax.bar(x, values, color=colors, yerr=error_bars, capsize=4, edgecolor="white", width=0.6)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=30, ha="right")
        ax.set_xlabel(spec.get("x_label", ""))
        ax.set_ylabel(spec.get("y_label", ""))
        if show_values:
            for bar, v in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005, f"{v:.3f}", ha="center")

    y_range = spec.get("y_range")
    if y_range:
        if horizontal:
            ax.set_xlim(y_range)
        else:
            ax.set_ylim(y_range)


def _draw_grouped_bar(ax: plt.Axes, spec: dict[str, Any], palette: list[str]) -> None:
    """グループ化棒グラフを描画する."""
    categories = spec["categories"]
    groups = spec["groups"]
    show_values = spec.get("show_values", True)
    n_groups = len(groups)
    x = np.arange(len(categories))
    width = 0.8 / n_groups

    for i, g in enumerate(groups):
        offset = (i - n_groups / 2 + 0.5) * width
        bars = ax.bar(x + offset, g["values"], width, label=g["label"], color=palette[i % len(palette)], edgecolor="white")
        if show_values:
            for bar, v in zip(bars, g["values"]):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.003, f"{v:.3f}", ha="center", fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=30, ha="right")
    ax.set_xlabel(spec.get("x_label", ""))
    ax.set_ylabel(spec.get("y_label", ""))
    ax.legend(loc="best")

    y_range = spec.get("y_range")
    if y_range:
        ax.set_ylim(y_range)


def _draw_line(ax: plt.Axes, spec: dict[str, Any], palette: list[str]) -> None:
    """折れ線グラフを描画する."""
    values = spec["values"]
    x_values = spec.get("x_values") or list(range(len(values)))

    ax.plot(x_values, values, color=palette[0], marker="o", markersize=4)
    ax.set_xlabel(spec.get("x_label", ""))
    ax.set_ylabel(spec.get("y_label", ""))

    y_range = spec.get("y_range")
    if y_range:
        ax.set_ylim(y_range)


def _draw_multi_line(ax: plt.Axes, spec: dict[str, Any], palette: list[str]) -> None:
    """複数折れ線グラフを描画する."""
    series = spec["series"]
    x_values = spec.get("x_values") or list(range(1, len(series[0]["values"]) + 1))
    markers = ["o", "s", "^", "D", "v", "p", "*", "h"]

    for i, s in enumerate(series):
        ax.plot(
            x_values,
            s["values"],
            label=s["label"],
            color=palette[i % len(palette)],
            marker=markers[i % len(markers)],
            markersize=5,
        )

    ax.set_xlabel(spec.get("x_label", "Epoch"))
    ax.set_ylabel(spec.get("y_label", ""))
    ax.legend(loc="best")

    y_range = spec.get("y_range")
    if y_range:
        ax.set_ylim(y_range)


# ---------------------------------------------------------------------------
# ディスパッチ
# ---------------------------------------------------------------------------

CHART_HANDLERS = {
    "learning_curve": _draw_learning_curve,
    "confusion_matrix": _draw_confusion_matrix,
    "bar": _draw_bar,
    "grouped_bar": _draw_grouped_bar,
    "line": _draw_line,
    "multi_line": _draw_multi_line,
}


def generate_chart(spec: dict[str, Any], output_override: str | None = None) -> Path:
    """1 つのチャート定義から PNG を生成し、出力パスを返す."""
    chart_type = spec.get("chart_type")
    if chart_type not in CHART_HANDLERS:
        raise ValueError(f"Unknown chart_type: {chart_type!r}. Supported: {list(CHART_HANDLERS.keys())}")

    output_path = Path(output_override or spec.get("output_path", "chart.png"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    style = spec.get("style", "default")
    lang = spec.get("lang", "ja")
    palette = _apply_style(style, lang)

    figsize = tuple(spec.get("figsize", [10, 6]))
    dpi = spec.get("dpi", 150)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_title(spec.get("title", ""))

    CHART_HANDLERS[chart_type](ax, spec, palette)

    fig.tight_layout()
    fig.savefig(str(output_path), bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"[chart-generator] Saved: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="JSON 定義から PNG チャートを生成する")
    parser.add_argument("--input", required=True, help="チャート定義 JSON ファイルのパス")
    parser.add_argument("--output", default=None, help="出力 PNG パス（単一チャート時、JSON 内の output_path より優先）")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    if isinstance(data, list):
        for i, spec in enumerate(data):
            generate_chart(spec)
        print(f"[chart-generator] {len(data)} charts generated.")
    else:
        generate_chart(data, output_override=args.output)


if __name__ == "__main__":
    main()
