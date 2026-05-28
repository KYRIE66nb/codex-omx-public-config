---
name: data-analysis
description: Analyze datasets with spreadsheets, Python stats, plots, and reports.
---

# Data Analysis

Use this skill when the user asks to analyze data, spreadsheets, CSV/XLSX files, experiment results, statistics, charts, dashboards, or model outputs.

## Routing

1. For `.xlsx`, `.xls`, or spreadsheet work, prefer the Spreadsheets plugin and `officecli-xlsx`.
2. For experiment metrics and result folders, use `analyze-results`.
3. For statistical tests and reporting, use `statistical-analysis`.
4. For regression, time series, diagnostics, or inference tables, use `statsmodels`.
5. For scientific computing, optimization, interpolation, or numerical routines, use `scipy`.
6. For symbolic formulas or exact derivations, use `sympy`.
7. For graph/network datasets, use `networkx`.
8. For publication-quality figures, use `plot-from-data`.

Always preserve source data, produce reproducible code or notebooks/scripts when analysis is non-trivial, and verify generated tables/figures against the input data.
