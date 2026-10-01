"""Loss concentration, loss-basis sensitivity, and the single exploratory
Kruskal-Wallis test (paper Sections V-F, V-I and V-J)."""
import numpy as np
import pandas as pd
from scipy import stats
from common import load, gini, LOSS, TABLES, SUPP

def shares(e):
    t = e[LOSS].sum()
    return {"incidents": len(e), "total_loss_usd": t, "median_loss_usd": e[LOSS].median(),
            "pf_cs_share": e[e.pattern_code.isin(["PF", "CS"])][LOSS].sum() / t,
            "fd3_fd5_share": e[e.domain_code.isin(["FD-3", "FD-5"])][LOSS].sum() / t,
            "pf_share": e[e.pattern_code == "PF"][LOSS].sum() / t,
            "cs_share": e[e.pattern_code == "CS"][LOSS].sum() / t}

def main():
    d = load()
    x = np.sort(d[LOSS].values); tot = x.sum(); n = len(x)
    conc = pd.Series({"gini": gini(x), "largest_incident_share": x[-1] / tot,
                      "top5_share": x[-5:].sum() / tot, "top10_share": x[-10:].sum() / tot,
                      "bottom_half_share": x[: n // 2].sum() / tot}, name="value")
    conc.to_csv(TABLES / "table_loss_concentration.csv")

    MINT = "Value of unbacked minted assets"
    REAL = "Real assets obtained with unbacked tokens"
    HELD = "Bridge-held assets withdrawn"
    lb = pd.DataFrame({
        "All incidents": shares(d),
        "Excluding unbacked-mint valuations": shares(d[d.loss_basis != MINT]),
        "Excluding all unbacked-token bases": shares(d[~d.loss_basis.isin([MINT, REAL])]),
        "Bridge-held assets withdrawn only": shares(d[d.loss_basis == HELD]),
    }).T
    lb.index.name = "incidents_included"
    lb.to_csv(TABLES / "table_loss_basis_sensitivity.csv")
    d.groupby("loss_basis")[LOSS].agg(["size", "sum"]).to_csv(SUPP / "loss_by_basis.csv")

    kw = stats.kruskal(*[g[LOSS] for _, g in d.groupby("pattern_code")])
    pd.Series({"test": "Kruskal-Wallis, gross loss by primary pattern", "H": kw.statistic,
               "df": d.pattern_code.nunique() - 1, "p_value": kw.pvalue,
               "note": "Exploratory only; not a confirmatory test."}).to_csv(TABLES / "table_kruskal_wallis.csv")

    print("== Loss analysis =="); print(conc.round(4).to_string()); print(lb.round(4).to_string())
    print(f"Kruskal-Wallis H({d.pattern_code.nunique()-1}) = {kw.statistic:.2f}, p = {kw.pvalue:.3f}")

if __name__ == "__main__":
    main()
