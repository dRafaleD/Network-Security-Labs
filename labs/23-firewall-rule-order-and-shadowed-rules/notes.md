# Day 23 — Firewall Rule Order and Shadowed Rules

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Firewall Rule Order and Shadowed Rules** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Most firewalls use first-match evaluation, so rule order changes the outcome.
2. A narrower rule placed after a broader one with the same port may never be reached.
3. End the rule set with an explicit default deny and test with real rule-hit counters.

## Important distinctions
- Finding an indicator does not validate every inference about it.
- Identify the trust boundary and the party controlling each input.
- Use both positive and negative cases; document measurement limitations.

## Hands-on lab
Read `firewall_demo.py` before running the following from this lab folder:

~~~bash
python3 firewall_demo.py
~~~

## Assignments
1. Predict the output from the code.
2. Run the program and record inputs and outputs.
3. Change a harmless input and explain the resulting difference.
4. Add an assertion for one security property.
5. Describe a negative case and a potential false positive.
6. Propose an independent corroboration method.

## Knowledge check
1. Where does the input originate?
2. What was directly observed?
3. What assumptions might fail in production?
4. Which evidence would be insufficient?
5. What should an automated test check?

## Safety and limitations
Use only authorized systems and synthetic data. The example is not a complete security or detection product.
