# Day 31 — SYN Flood: Half-Open Connection Ratio

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **SYN Flood: Half-Open Connection Ratio** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. A SYN flood leaves many connections half open: SYNs arrive, but handshakes never complete.
2. Compare SYN count to completed handshakes per destination; a very low completion ratio is a signal.
3. SYN cookies and rate limits are mitigations; detection tells you when to apply them.

## Important distinctions
- Port scans also produce unanswered SYNs but across many ports.
- A server under load can look similar to a flood.
- Spoofed source addresses make attribution unreliable.

## Hands-on lab
Read `synflood_demo.py` before running the following from this lab folder:

~~~bash
python3 synflood_demo.py
~~~


## Assignments
1. Predict which destination is flagged.
2. Run the demo and record the completion ratios.
3. Lower the threshold and describe the false positives.
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
