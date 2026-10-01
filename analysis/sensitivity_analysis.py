"""Boundary-case sensitivity analysis (paper Section V-H): every boundary case is
switched between its primary and alternative label, giving 2^6 = 64
combinations. Also checks the effect of excluding the E4 (inferred) incident."""
import itertools
import pandas as pd
from common import load, alternatives, LOSS, TABLES, SUPP

def main():
    d = load(); tot = d[LOSS].sum()
    alt = alternatives(d)
    rows = []
    for combo in itertools.product([0, 1], repeat=len(alt)):
        e = d.copy()
        switched = []
        for flag, (iid, (p, f)) in zip(combo, alt.items()):
            if flag:
                e.loc[e.incident_id == iid, ["pattern_code", "domain_code"]] = [p, f]
                switched.append(iid)
        cnt = e.pattern_code.value_counts()
        top2 = set(cnt.sort_values(ascending=False).index[:2])
        rows.append({"switched_incidents": ";".join(switched) or "none",
                     **{f"n_{p}": int(cnt.get(p, 0)) for p in ["PF", "LE", "EI", "ESM", "CS", "IH"]},
                     "pf_cs_loss_share": e[e.pattern_code.isin(["PF", "CS"])][LOSS].sum() / tot,
                     "fd3_fd5_loss_share": e[e.domain_code.isin(["FD-3", "FD-5"])][LOSS].sum() / tot,
                     "pf_cs_two_most_common": top2 == {"PF", "CS"}})
    r = pd.DataFrame(rows)
    r.to_csv(SUPP / "sensitivity_64_combinations.csv", index=False)
    summary = pd.DataFrame({
        "reported": [13, 13, r.pf_cs_loss_share.iloc[0], r.fd3_fd5_loss_share.iloc[0], True, 3, 3],
        "minimum": [r.n_PF.min(), r.n_CS.min(), r.pf_cs_loss_share.min(), r.fd3_fd5_loss_share.min(),
                    r.pf_cs_two_most_common.all(), r.n_ESM.min(), r.n_IH.min()],
        "maximum": [r.n_PF.max(), r.n_CS.max(), r.pf_cs_loss_share.max(), r.fd3_fd5_loss_share.max(),
                    r.pf_cs_two_most_common.all(), r.n_ESM.max(), r.n_IH.max()],
    }, index=["PF incidents", "CS incidents", "PF and CS share of total loss",
              "FD-3 and FD-5 share of total loss", "PF and CS two most common (all 64)",
              "ESM incidents", "IH incidents"])
    summary.to_csv(TABLES / "table_sensitivity.csv")

    e = d[d.evidence_level != "E4"]; t = e[LOSS].sum()
    print("== Sensitivity analysis ==")
    print(summary.to_string())
    print("Excluding E4:", f"PF+CS {e[e.pattern_code.isin(['PF','CS'])][LOSS].sum()/t:.3%},",
          f"FD-3+FD-5 {e[e.domain_code.isin(['FD-3','FD-5'])][LOSS].sum()/t:.3%}")

if __name__ == "__main__":
    main()
