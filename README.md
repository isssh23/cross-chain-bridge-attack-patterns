# Trust-Violation Attack Patterns in Cross-Chain Bridges

Data, codebook, and analysis scripts accompanying the paper:

> I. Samiha, Y. Rahman, and R. Mukta, *Attack Patterns in Cross-chain Bridges* (manuscript under submission).

## Overview

The study analyses **48 verified cross-chain bridge incidents** recorded between **January 2022 and August 2026**, representing **\$2.676 billion** in gross bridge-specific losses. Each incident is classified by the bridge trust assumption the attacker violates (one of six attack patterns) and by where the compromised trust boundary lies (one of five functional domains).

**Attack patterns**

| Group | Patterns |
|---|---|
| A – Verification and Contract Logic | Proof Forgery (PF), Logic Exploitation (LE) |
| B – Cross-Chain Information and Economic State | Event Injection (EI), Economic-State Manipulation (ESM) |
| C – Operational Trust Compromise | Credential Seizure (CS), Infrastructure Hijacking (IH) |

**Functional domains**: FD-1 Deposit, FD-2 Relay, FD-3 Verification, FD-4 Execution, FD-5 Governance & Operations.

## Repository contents

- `data/` – incident dataset, excluded candidates, sources, and data dictionary
- `codebook/` – inclusion rules, pattern and domain definitions, boundary rules
- `analysis/` – scripts used for the analyses reported in the paper
- `results/` – tables and figures produced by the scripts
- `manuscript/` – LaTeX source of the paper
- `supplementary/` – supplementary tables

## Reproducibility map

| Paper component | Repository location |
|---|---|
| 48-incident dataset | `data/incidents.csv` |
| Excluded candidates (12) | `data/excluded_incidents.csv` |
| Evidence sources | `data/sources.csv` |
| Variable definitions | `data/data_dictionary.csv` |
| Inclusion, evidence, and loss rules | `codebook/codebook.md` |
| Attack-pattern definitions and criteria | `codebook/attack_patterns.md` |
| Functional-domain coding questions | `codebook/functional_domains.md` |
| Boundary rules and boundary cases | `codebook/boundary_cases.md` |
| Dataset overview, pattern and domain distributions, heatmap | `analysis/descriptive_analysis.py` |
| Yearly distribution and figures | `analysis/temporal_analysis.py` |
| Loss concentration, loss-basis sensitivity, exploratory test | `analysis/loss_analysis.py` |
| Boundary-case sensitivity (64 combinations) | `analysis/sensitivity_analysis.py` |
| Tables | `results/tables/` |
| Figures | `results/figures/` |
| All 64 sensitivity combinations | `supplementary/supplementary_tables/sensitivity_64_combinations.csv` |

## Running the analysis

Requires Python 3.9 or later.

```bash
pip install -r requirements.txt
python analysis/generate_tables.py
```

This runs every analysis script and writes the tables to `results/tables/`, the figures to `results/figures/`, and the supplementary tables to `supplementary/supplementary_tables/`. The scripts reproduce the descriptive statistics, loss analysis, temporal analysis, and sensitivity analyses reported in the paper.

## Notes on interpretation

- The 48 incidents are an observed corpus built with the inclusion criteria in `codebook/codebook.md`, not a complete or random sample of all bridge attacks. Results are descriptive and are not population-level attack rates.
- 2026 covers January to August only.
- Loss figures are gross: recoveries are not subtracted. The `loss_basis` field records what each figure measures, and the paper reports how the results change under alternative loss bases.

## License

Code is released under the MIT License, and data and documentation under CC BY 4.0. See `LICENSE`.

## Citation

If you use this dataset or code, please cite the paper (see `CITATION.cff`).
