"""Incidents and losses per year, and the two yearly figures (paper Section V-B).
2026 covers January to August only; counts are not attack rates."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common import load, PATTERNS, LOSS, TABLES, FIGURES

plt.rcParams.update({"font.family": "serif", "font.size": 8,
                     "axes.spines.top": False, "axes.spines.right": False})
COLORS = {"PF": "#1f4e79", "LE": "#6fa8dc", "EI": "#38761d", "ESM": "#93c47d", "CS": "#990000", "IH": "#e06666"}

def main():
    d = load()
    g = d.groupby("year")[LOSS]
    yearly = pd.DataFrame({"months_observed": [8 if y == 2026 else 12 for y in sorted(d.year.unique())],
                           "incidents": g.size(), "total_loss_usd": g.sum(),
                           "median_loss_usd": g.median(), "q1_loss_usd": g.quantile(0.25),
                           "q3_loss_usd": g.quantile(0.75)}, index=sorted(d.year.unique()))
    yearly["share_of_total_loss"] = yearly["total_loss_usd"] / d[LOSS].sum()
    yearly.index.name = "year"
    yearly.to_csv(TABLES / "table_yearly.csv")
    xt = pd.crosstab(d["year"], d["pattern_code"]).reindex(columns=PATTERNS, fill_value=0)
    xt.to_csv(TABLES / "table_pattern_by_year.csv")
    labels = [str(y) if y != 2026 else "2026*" for y in xt.index]

    fig, ax = plt.subplots(figsize=(3.5, 2.2))
    bottom = np.zeros(len(xt))
    for p in PATTERNS:
        ax.bar(labels, xt[p], bottom=bottom, color=COLORS[p], label=p, width=0.6)
        bottom += xt[p].values
    for i, v in enumerate(bottom):
        ax.text(i, v + 0.3, str(int(v)), ha="center", fontsize=7)
    ax.set_ylabel("Number of incidents"); ax.set_ylim(0, bottom.max() + 4)
    ax.legend(ncol=3, fontsize=6.5, frameon=False, loc="upper left")
    fig.tight_layout(); fig.savefig(FIGURES / "incidents_by_year.pdf"); fig.savefig(FIGURES / "incidents_by_year.png", dpi=200); plt.close(fig)

    yl = yearly[["total_loss_usd", "median_loss_usd"]] / 1e6
    fig, ax = plt.subplots(figsize=(3.5, 2.2))
    x = np.arange(len(yl)); w = 0.38
    b1 = ax.bar(x - w / 2, yl["total_loss_usd"], w, color="#1f4e79", label="Total loss")
    b2 = ax.bar(x + w / 2, yl["median_loss_usd"], w, color="#9fc5e8", label="Median loss")
    ax.set_yscale("log"); ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel("Loss (USD million, log scale)")
    for bars in (b1, b2):
        for r in bars:
            h = r.get_height()
            ax.text(r.get_x() + r.get_width() / 2, h * 1.15, f"{h:,.0f}" if h >= 10 else f"{h:.1f}", ha="center", fontsize=6)
    ax.set_ylim(0.5, yl["total_loss_usd"].max() * 4)
    ax.legend(fontsize=6.5, frameon=False, loc="upper right")
    fig.tight_layout(); fig.savefig(FIGURES / "loss_by_year.pdf"); fig.savefig(FIGURES / "loss_by_year.png", dpi=200); plt.close(fig)

    print("== Temporal analysis =="); print(yearly.round(3).to_string()); print(xt.to_string())

if __name__ == "__main__":
    main()
