"""Run every analysis and regenerate all tables and figures.

Usage (from the repository root):
    python analysis/generate_tables.py
"""
import descriptive_analysis, temporal_analysis, loss_analysis, sensitivity_analysis

if __name__ == "__main__":
    for m in (descriptive_analysis, temporal_analysis, loss_analysis, sensitivity_analysis):
        m.main()
        print()
    print("Tables written to results/tables/, figures to results/figures/, "
          "and supplementary tables to supplementary/supplementary_tables/.")
