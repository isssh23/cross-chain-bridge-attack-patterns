# Data

| File | Contents |
|---|---|
| `incidents.csv` | The 48 verified incidents (January 2022 – August 2026), one row per incident, with pattern and domain labels, gross bridge-specific loss, loss basis, evidence level, rationale, and boundary-case information. |
| `excluded_incidents.csv` | The 12 candidate incidents that were excluded, with their sources and the reason for exclusion. |
| `sources.csv` | Public evidence sources for each incident, linked by `incident_id` and `source_id`. |
| `data_dictionary.csv` | Definition and allowed values of every variable. |
| `Bridge_Attack_Dataset_Final.xlsx` | The working spreadsheet from which the CSV files were exported. It also contains the Summary sheet (live formulas), the codebook, the change log, and blank columns for an independent second coder. |

Notes:
- Each incident has exactly one primary attack pattern and one primary functional domain, so counts and losses sum to the dataset totals.
- All monetary values are gross bridge-specific losses in US dollars at the time of the incident. Recovered funds are not subtracted. See `codebook/codebook.md`.
- All sources are publicly available web pages; no private data are included.
