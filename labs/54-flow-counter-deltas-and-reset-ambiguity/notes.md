# Day 54 — Flow Counter Deltas and Reset Ambiguity

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](counter_deltas.py)

Day 53 classified fictional flow summaries. Today distinguish a cumulative byte counter from a per-window delta. Within one origin and boot epoch, a monotonic counter yields the difference. An epoch change, time reversal or counter regression does not justify inventing a byte count.

Worked examples from 100 bytes at time 10: 160 at time 20 gives 60 bytes; 100 gives zero; 90 gives COUNTER_REGRESSION; a different boot gives RESET_BOUNDARY even if its counter is larger.

**Practice:** construct three samples from one epoch and sum valid deltas. Add a reset and explain why the unobserved boundary traffic cannot be recovered. Distinguish reset, wraparound and collector error; this example deliberately makes no automatic wrap correction. Ten scenarios, no real network or interfaces.

## Run
```bash
python3 labs/54-flow-counter-deltas-and-reset-ambiguity/counter_deltas.py
```
