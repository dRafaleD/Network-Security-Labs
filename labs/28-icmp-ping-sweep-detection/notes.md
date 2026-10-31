# Day 28 — ICMP Ping Sweep Detection

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **ICMP Ping Sweep Detection** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. A ping sweep is one source sending echo requests to many different hosts in a short window.
2. Count distinct destinations per source inside a sliding time window.
3. Monitoring systems also ping many hosts, so keep an owner-tagged allow-list.

## Important distinctions
- Repeated pings to one host are a different pattern (availability checks).
- A sweep shows interest in the network, not an intrusion by itself.
- The window length decides whether slow sweeps are caught.

## Hands-on lab
Read `sweep_demo.py` before running the following from this lab folder:

~~~bash
python3 sweep_demo.py
~~~


## Assignments
1. Predict which sources are flagged.
2. Run the demo and record the distinct-destination counts.
3. Stretch the sweep over a longer time and see when detection stops.
4. Add an assertion for one security property.
5. Describe a negative case and a potential false positive.
6. Propose an independent corroboration method.

## Knowledge check
1. Where does the input originate, and who controls it?
2. What was directly observed, as opposed to inferred?
3. What assumptions might fail in production?
4. Which evidence would be insufficient on its own?
5. What should an automated test check?

## Safety and limitations
Use only authorized systems and synthetic data. The example is not a complete security or detection product.
