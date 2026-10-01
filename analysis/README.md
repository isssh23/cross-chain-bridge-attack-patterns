# Analysis scripts

Run all analyses from the repository root:

```bash
python analysis/generate_tables.py
```

| Script | Paper section | Outputs |
|---|---|---|
| `descriptive_analysis.py` | V-A, V-C, V-D, V-E | Dataset overview, loss by pattern, domain, and group, Wilson intervals, pattern × domain matrix, `heatmap` figure |
| `temporal_analysis.py` | V-B | Yearly table, pattern-by-year table, `incidents_by_year` and `loss_by_year` figures |
| `loss_analysis.py` | V-F, V-I, V-J | Loss concentration (Gini, top-k shares), loss-basis sensitivity, Kruskal–Wallis test |
| `sensitivity_analysis.py` | V-H | Boundary-case sensitivity summary and all 64 label combinations |
| `common.py` | – | Shared paths and helper functions |

Each script can also be run on its own, e.g. `python analysis/loss_analysis.py`.
