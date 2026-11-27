# Day 56 — Weighted Flow Rates and Coverage Reporting

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](weighted_rates.py)

Day 55 normalized individual counter deltas. Aggregate only validated, nonoverlapping intervals of one fictional stream. Divide total bytes by total covered seconds, not the unweighted mean of interval rates. For 100 bytes over 2 seconds and 100 over 8 seconds, the correct weighted rate is 20 bytes/s, not 31.25. Gaps are reported separately as covered duration / total span; missing intervals are not zero traffic. Eight cases include gaps, overlaps, empty input and fractional rates. Add a gap and compare coverage. The input assumes already validated deltas from a single stream; no live traffic, scanning or attribution.

## Run
```bash
python3 labs/56-weighted-flow-rates-and-coverage-reporting/weighted_rates.py
```
