"""Dataset overview, attack-pattern and functional-domain distributions,
group-level totals, and the pattern x domain heatmap (paper Sections V-A, V-C,
V-D and V-E)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common import load, summarise, wilson, PATTERNS, DOMAINS, LOSS, TABLES, FIGURES

plt.rcParams.update({"font.family": "serif", "font.size": 8})

def main():
    d = load()
    n, tot = len(d), d[LOSS].sum()
    overview = pd.Series({
        "verified_incidents": n,
        "affected_systems": d["affected_system_id"].nunique(),
        "systems_attacked_more_than_once": d.groupby("affected_system_id").size().gt(1).sum(),
        "total_gross_loss_usd": tot,
        "median_gross_loss_usd": d[LOSS].median(),
        "q1_gross_loss_usd": d[LOSS].quantile(0.25),
        "q3_gross_loss_usd": d[LOSS].quantile(0.75),
        "mean_gross_loss_usd": d[LOSS].mean(),
        "incidents_loss_ge_100m": int((d[LOSS] >= 100e6).sum()),
    }, name="value")
    overview.to_csv(TABLES / "table_dataset_overview.csv")

    pat = summarise(d, "pattern_code").reindex(PATTERNS)
    pat.to_csv(TABLES / "table_loss_by_pattern.csv")
    dom = summarise(d, "domain_code").reindex(DOMAINS)
    dom.to_csv(TABLES / "table_loss_by_domain.csv")
    grp = summarise(d, "group")
    grp.to_csv(TABLES / "table_loss_by_group.csv")

    k_pfcs = d["pattern_code"].isin(["PF", "CS"]).sum()
    k_fd35 = d["domain_code"].isin(["FD-3", "FD-5"]).sum()
    rows = []
    for label, k in [("PF and CS incidents", k_pfcs), ("FD-3 and FD-5 incidents", k_fd35)]:
        lo, hi = wilson(k, n)
        rows.append({"finding": label, "count": k, "share": k / n, "wilson_low": lo, "wilson_high": hi})
    pd.DataFrame(rows).to_csv(TABLES / "table_wilson_intervals.csv", index=False)

    ct = pd.crosstab(d["pattern_code"], d["domain_code"]).reindex(index=PATTERNS, columns=DOMAINS, fill_value=0)
    lt = d.pivot_table(index="pattern_code", columns="domain_code", values=LOSS,
                       aggfunc="sum", fill_value=0).reindex(index=PATTERNS, columns=DOMAINS, fill_value=0)
    ct.to_csv(TABLES / "table_pattern_domain_counts.csv")
    lt.to_csv(TABLES / "table_pattern_domain_losses.csv")

    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.imshow(ct.values, cmap="Blues", vmin=0, aspect="auto")
    ax.set_xticks(range(5))
    ax.set_xticklabels(["FD-1\nDeposit", "FD-2\nRelay", "FD-3\nVerify", "FD-4\nExecute", "FD-5\nGov. & Ops."], fontsize=6.5)
    ax.set_yticks(range(6)); ax.set_yticklabels(PATTERNS)
    for i in range(6):
        for j in range(5):
            c = ct.values[i, j]
            if c:
                col = "white" if c > ct.values.max() * 0.55 else "black"
                v = lt.values[i, j] / 1e6
                ax.text(j, i - 0.12, str(c), ha="center", va="center", fontsize=8, fontweight="bold", color=col)
                ax.text(j, i + 0.22, f"${v:,.0f}M" if v >= 1 else f"${v:.2f}M", ha="center", va="center", fontsize=5.5, color=col)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks(np.arange(-.5, 5), minor=True); ax.set_yticks(np.arange(-.5, 6), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5); ax.tick_params(which="minor", length=0)
    fig.tight_layout(); fig.savefig(FIGURES / "heatmap.pdf"); fig.savefig(FIGURES / "heatmap.png", dpi=200); plt.close(fig)

    print("== Descriptive analysis ==")
    print(overview.to_string())
    print(pat.round(4).to_string()); print(dom.round(4).to_string())

if __name__ == "__main__":
    main()
