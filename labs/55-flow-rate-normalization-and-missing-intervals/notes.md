# Day 55 — Flow Rate Normalization and Missing Intervals

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](rate_review.py)

Day 54 examined counter deltas and reset ambiguity. Today normalize byte deltas by elapsed time, using exact fractions in a fictional collector. Equal byte increments over different intervals yield different rates. A changed boot, regressed counter or gap longer than ten toy seconds does not produce a rate. Compare 100 bytes over two and five seconds, predict all 11 cases, and add a fractional rate. The gap threshold is a teaching choice, not a standard. A computed average cannot reveal bursts or establish exfiltration. No packet capture, scanning or network access.

## Run
```bash
python3 labs/55-flow-rate-normalization-and-missing-intervals/rate_review.py
```
