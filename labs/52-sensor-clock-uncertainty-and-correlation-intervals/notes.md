# Day 52 — Sensor Clock Uncertainty and Correlation Intervals

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](clock_intervals.py)

Day 51 compared point timestamps from registered sensors. Day 52 models bounded clock uncertainty as closed intervals. For one fictional event, all distinct origins must share a possible common time. Repeated copies from one origin count once. Disjoint intervals or contradictory event labels prevent correlation. Overlap yields POSSIBLE_TIME_MATCH, not proof that an event is identical.

**Questions:** How does clock uncertainty differ from delivery latency? Why check a shared intersection rather than just a chain of pairwise overlaps? Why does time agreement not establish an independent physical sensor?

Origin labels and intervals are assumed to be provided by a trusted collector. No packet capture, scanning, real keys or authentication implementation.

## Run
```bash
python3 labs/52-sensor-clock-uncertainty-and-correlation-intervals/clock_intervals.py
```
