# Day 57 — Flow Window Coverage and Overlap

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](window_coverage.py)

Day 56 introduced weighted rates and coverage. Today compute the union of half-open observation windows rather than counting overlapping seconds twice. Two windows [0,6) and [4,10) cover ten seconds, not twelve. Coverage does not authorize adding their byte counters: overlap requires separate review. Predict ten cases, add out-of-order windows and compare an empty capture with complete coverage. Coverage is only declared temporal coverage, not proof every packet was recorded. No packet capture, real network access or scanning.

## Run
```bash
python3 labs/57-flow-window-coverage-and-overlap/window_coverage.py
```
