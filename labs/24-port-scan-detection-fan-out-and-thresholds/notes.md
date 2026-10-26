# Day 24 — Port Scan Detection: Fan-Out and Thresholds

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Port Scan Detection: Fan-Out and Thresholds** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. A port scan shows up as one source touching many ports on one host; a sweep is one source touching many hosts on one port.
2. Count distinct destinations and ports per source instead of raw connection counts.
3. Thresholds trade missed slow scans against false alarms from scanners and monitoring tools.

## Important distinctions
- Many connections to one port are repeated traffic, not scanning.
- A low-and-slow scan stays under a short window threshold; the window length matters.
- Authorized vulnerability scanners produce the same pattern and need an allow-list with owners.

## Hands-on lab
Read `scan_demo.py` before running the following from this lab folder:

~~~bash
python3 scan_demo.py
~~~


## Assignments
1. Predict which of the three source hosts raise an alert.
2. Run the demo and record each alert.
3. Lower `port_threshold` to 5 and describe which new false positives could appear.
4. Add an assertion that a source touching exactly 19 ports is not flagged at the default threshold.
5. Describe how a slow scan could evade the demo and how a time window helps.
6. Propose an independent data source (firewall deny logs, IDS) to corroborate an alert.

## Knowledge check
1. Where does the input originate, and who controls it?
2. What was directly observed, as opposed to inferred?
3. What assumptions might fail in production?
4. Which evidence would be insufficient on its own?
5. What should an automated test check?

## Safety and limitations
Use only authorized systems and synthetic data. The example is not a complete security or detection product.
