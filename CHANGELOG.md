# Changelog

## v1.0.0 – Data and code accompanying manuscript submission

Initial public release: 48 verified incidents, 12 excluded candidates, codebook, and analysis scripts.

### Dataset construction history

The changes below were made while building the dataset, before this release. They are also recorded in the Change Log sheet of `data/Bridge_Attack_Dataset_Final.xlsx`.

- **FLA → ESM**: Attack Pattern changed to Economic-State Manipulation (ESM) for Allbridge Core (Jul 2026), Shibarium (Sep 2025) and Allbridge (Apr 2023); rationale text rewritten so it no longer refers to Flash Loan Amplification and frames the flash loan as an enabler.
- **2021 contamination**: PolkaBridge, pNetwork, Poly Network, ChainSwap and THORChain (2021) moved to Excluded Incidents (outside study period); their old ST-x codes remapped to FD-x there for consistency.
- **Non-bridge incidents**: Poloniex, Stake.com, KyberSwap Elastic moved to Excluded Incidents per the reviewer. By the same inclusion rule, Poolz Finance (locker-contract overflow) and Pike Finance 2nd incident (proxy-upgrade storage collision) were also excluded — both exploited non-bridge components. Review these two if you disagree; restoring them is a copy-paste.
- **Cross-chain vs bridge scope**: Bridge-only scope adopted and written into the Codebook. Mixin excluded (cloud-provider compromise of custodial material, not a bridge mechanism). Garden excluded (solver-owned assets; no protocol or user loss per Garden's report).
- **Loss normalization**: New numeric column "Bridge-Specific Loss (USD)" plus a note column. HECO now counts $86.8M bridge loss only (HTX exchange losses removed from figure and from the rationale). Kelp counts the $292M bridge drain only. Sandbox counts the ~$697K direct drain. Across counts the $4.5M paid out. Ranges use the lower bound.
- **Terminology**: "Primary Lifecycle Stage" renamed "Primary Functional Domain"; "Reason (Why This Pattern & Stage)" renamed accordingly; two rationales that said "stage" reworded. Codebook defines FD-1–FD-4 as the sequential path and FD-5 as the control plane.
- **Evidence structure**: New "Evidence Level" column (E1–E4) for every record and a Scope / Evidence Note for borderline rows. Saga previously had one source (Halborn) and did not meet the evidence rule; The Block report added as Source 2. TeleSwap flagged E4 (root cause undisclosed).
- **Other cleanup**: Dates normalised to real dates (ranges use start date, noted); Year column added; stable IDs (BR-001…); Verus repeat-attack text no longer refers to "incident #8 above"; Hyperbridge root-cause label "Admin Permission Takeover" changed to "Proof Verification Flaw" to match its own description and PF code; truncated THORChain 2021 URL flagged.
- **Dataset count**: 60 rows → 55 in study period → 48 bridge-only incidents. The paper's "44" must be updated to 48 (or the 4-incident difference explicitly justified).
- **Domain labels**: FD-3 Verification → FD-3 Verification; FD-4 Execution → FD-4 Execution; FD-5 Governance & Operations → FD-5 Governance & Operations (Dataset, Excluded Incidents, Summary, Codebook) to match the paper.
- **Loss terminology**: Column F renamed 'Gross Bridge-Specific Loss (USD)'; Summary and Codebook updated to state that recoveries are not subtracted. Values unchanged.
- **Enabling mechanisms**: New column Q records supporting methods (e.g., flash loans in 4 incidents) taken only from the existing root-cause text. No pattern labels changed.
- **Boundary cases**: New columns R–T flag the six boundary cases (BR-003, BR-014, BR-021, BR-024, BR-027, BR-041) and record their alternative labels for the sensitivity analysis.
- **Classification confidence**: New formula column U (High / Medium / Low) based on evidence level and boundary status.
- **Inter-rater reliability**: New blank input columns V–W for an independent second coder, with automatic raw agreement and Cohen's kappa on the Summary sheet.
- **Loss concentration**: Summary sheet now reports largest-incident, top-5 and top-10 loss shares and the Gini coefficient as live formulas.
- **Loss basis**: New column X records the basis of each gross loss figure (5 categories) from the existing notes; Summary sheet reports counts and totals by basis. Loss values unchanged.
