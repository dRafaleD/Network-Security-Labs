# Day 42 — IPv6 Conflict Timelines and Clock Uncertainty

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](clock_correlation_demo.py)

## Day 41 follow-up
A DAD failure and a different MAC observation near the same IPv6 address may be related. But event clocks may disagree. This lab models an **uncertainty interval** around each timestamp rather than treating seconds as exact.

A pair is **DEFINITELY_NEAR** if even the largest possible time gap is within the five-second window; **POSSIBLY_NEAR** if some possible time gap fits; otherwise **OUTSIDE_WINDOW**. Address, MAC and event-type checks run first.

## Run
```bash
python3 labs/42-ipv6-conflict-timeline-and-clock-uncertainty/clock_correlation_demo.py
```

## Exercises
1. How does timestamp uncertainty change a five-second correlation?
2. Why is a possible-time match weaker than a definite-time match?
3. Which NTP or device log evidence could reduce uncertainty?
4. Why can't a DAD failure and different MAC identify a malicious host?

## Limitations
All IPv6 addresses use documentation space; no socket or interface is accessed. Clock uncertainty here is symmetric and simplified. No conflict claim is proof of spoofing.
