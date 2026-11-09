"""Figures du rapport (PNG statiques ; les tableaux CSV servent de vue tableau)."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
SERIES = "#2a78d6"
DIVERGING = LinearSegmentedColormap.from_list(
    "bleu_rouge", ["#184f95", "#6da7ec", "#f0efec", "#ee8a89", "#b52f2f"])

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": INK_2, "xtick.color": INK_2,
    "ytick.color": INK_2, "text.color": INK, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
})

LABELS = {
    "global": "Global", "cardiovasculaire": "Cardiovasculaire", "metabolique": "Métabolique",
    "renal": "Rénal", "hepatique": "Hépatique",
    "inflammatoire_hematologique": "Inflammatoire / hémato.", "ref": "Âge + sexe",
}


def _label(name: str) -> str:
    return LABELS.get(name, name)


def calibration_grid(tables: dict[str, pd.DataFrame], horizon_years: int, path: Path):
    n = len(tables)
    cols = min(3, n)
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(3.6 * cols, 3.4 * rows), squeeze=False)
    for ax, (name, t) in zip(axes.flat, tables.items()):
        hi = max(t["predit"].max(), t["observe_ic95_haut"].max()) * 1.08
        ax.plot([0, hi], [0, hi], color=INK_2, lw=1, ls="--", zorder=1)
        ax.errorbar(t["predit"], t["observe"],
                    yerr=[t["observe"] - t["observe_ic95_bas"], t["observe_ic95_haut"] - t["observe"]],
                    fmt="o", ms=5, color=SERIES, ecolor=SERIES, elinewidth=1.2, capsize=0,
                    mec=SURFACE, mew=1.5, zorder=2)
        ax.set_xlim(0, hi)
        ax.set_ylim(0, hi)
        ax.set_title(_label(name))
        ax.set_xlabel(f"Risque prédit à {horizon_years} ans")
        ax.set_ylabel("Risque observé (Kaplan-Meier)")
    for ax in list(axes.flat)[n:]:
        ax.set_visible(False)
    fig.suptitle("Calibration en validation (déciles de risque prédit ; pointillé = parfait)",
                 x=0.01, ha="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def correlation_heatmap(corr: pd.DataFrame, path: Path, title: str):
    labels = [_label(c.removeprefix("gap_")) for c in corr.columns]
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    im = ax.imshow(corr.to_numpy(), cmap=DIVERGING, vmin=-1, vmax=1)
    ax.grid(False)
    ax.set_xticks(range(len(labels)), labels, rotation=35, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            v = corr.iat[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8,
                    color=SURFACE if abs(v) > 0.6 else INK)
    fig.colorbar(im, ax=ax, fraction=0.046, label="ρ de Spearman")
    fig.suptitle(title, x=0.02, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def forest(table: pd.DataFrame, label_col: str, path: Path, title: str, xlabel: str):
    t = table.iloc[::-1].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(6.4, 0.45 * len(t) + 1.2))
    y = np.arange(len(t))
    ax.axvline(1, color=INK_2, lw=1, ls="--")
    ax.hlines(y, t["ic95_bas"], t["ic95_haut"], color=SERIES, lw=2)
    ax.plot(t["HR"], y, "o", ms=7, color=SERIES, mec=SURFACE, mew=1.5)
    for yi, (hr, lo, hi) in enumerate(zip(t["HR"], t["ic95_bas"], t["ic95_haut"])):
        ax.text(t["ic95_haut"].max() * 1.02, yi, f"{hr:.2f} [{lo:.2f}–{hi:.2f}]",
                va="center", fontsize=8, color=INK_2)
    ax.set_yticks(y, [_label(s.removeprefix("gap_")) for s in t[label_col]])
    ax.set_xlabel(xlabel)
    ax.set_xlim(min(0.95, t["ic95_bas"].min() * 0.97), t["ic95_haut"].max() * 1.22)
    ax.grid(axis="y", visible=False)
    ax.set_title(title, loc="left")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def group_intervals(table: pd.DataFrame, est: str, lo: str, hi: str, ref: float,
                    band: tuple[float, float] | None, title: str, path: Path):
    """Point + IC par sous-groupe, un panneau par axe (petits multiples, une seule serie)."""
    axes_names = list(dict.fromkeys(table["axe"]))
    heights = [max(2, (table["axe"] == a).sum()) for a in axes_names]
    fig, axs = plt.subplots(len(axes_names), 1, figsize=(7.2, 0.42 * sum(heights) + 1.2),
                            gridspec_kw={"height_ratios": heights}, sharex=True, squeeze=False)
    xmin = min(table[lo].min(), band[0] if band else ref) * 0.97
    xmax = max(table[hi].max(), band[1] if band else ref) * 1.03 if table[hi].max() > 0 else 0.5
    for ax, a in zip(axs[:, 0], axes_names):
        t = table[table["axe"] == a].iloc[::-1].reset_index(drop=True)
        y = np.arange(len(t))
        if band:
            ax.axvspan(*band, color=GRID, alpha=0.6, lw=0)
        ax.axvline(ref, color=INK_2, lw=1, ls="--")
        ax.hlines(y, t[lo], t[hi], color=SERIES, lw=2)
        ax.plot(t[est], y, "o", ms=6, color=SERIES, mec=SURFACE, mew=1.5)
        labels = [f"{g} (n={n}, {d} décès)" for g, n, d in zip(t["groupe"], t["n"], t["deces"])]
        ax.set_yticks(y, labels, fontsize=8)
        ax.set_ylim(-0.6, len(t) - 0.4)
        ax.set_title(a, loc="left", fontsize=9)
        ax.grid(axis="y", visible=False)
        ax.set_xlim(xmin, xmax)
    fig.suptitle(title, x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
