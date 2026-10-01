"""Shared helpers for the analysis scripts.

All scripts read data/incidents.csv and write to results/ (tables and figures)
and supplementary/supplementary_tables/. Paths are resolved from the repository
root, so scripts can be run from any directory.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "incidents.csv"
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"
SUPP = ROOT / "supplementary" / "supplementary_tables"
for p in (TABLES, FIGURES, SUPP):
    p.mkdir(parents=True, exist_ok=True)

PATTERNS = ["PF", "LE", "EI", "ESM", "CS", "IH"]
DOMAINS = ["FD-1", "FD-2", "FD-3", "FD-4", "FD-5"]
GROUP = {"PF": "A", "LE": "A", "EI": "B", "ESM": "B", "CS": "C", "IH": "C"}
LOSS = "gross_loss_usd"

# Boundary cases and their alternative labels (pattern code, domain code),
# as recorded in data/incidents.csv (columns alternative_pattern / alternative_domain).
def load():
    d = pd.read_csv(DATA, parse_dates=["incident_date"])
    d["group"] = d["pattern_code"].map(GROUP)
    return d

def alternatives(d):
    b = d[d["boundary_case"] == "Yes"]
    return {r.incident_id: (r.alternative_pattern.split("(")[-1].rstrip(")"),
                            r.alternative_domain.split()[0])
            for r in b.itertuples()}

def wilson(k, n, z=1.959964):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h

def gini(values):
    x = np.sort(np.asarray(values, dtype=float))
    n = len(x)
    return 2 * np.sum(np.arange(1, n + 1) * x) / (n * x.sum()) - (n + 1) / n

def summarise(d, by):
    """Incidents, share, total, median and IQR (linear interpolation) of gross loss."""
    tot = d[LOSS].sum()
    g = d.groupby(by)[LOSS]
    out = pd.DataFrame({
        "incidents": g.size(),
        "share_incidents": g.size() / len(d),
        "total_loss_usd": g.sum(),
        "share_loss": g.sum() / tot,
        "median_loss_usd": g.median(),
        "q1_loss_usd": g.quantile(0.25),
        "q3_loss_usd": g.quantile(0.75),
    })
    return out
