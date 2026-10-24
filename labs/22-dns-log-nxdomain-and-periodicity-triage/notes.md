# Day 22 — DNS Log Triage: NXDOMAIN Ratio and Query Regularity

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **DNS Log Triage: NXDOMAIN Ratio and Query Regularity** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. A high NXDOMAIN ratio and very regular timing are triage leads, not verdicts.
2. Updaters, monitoring agents and misconfigured clients often look periodic.
3. Compare against a per-client baseline before raising an alert.

## Important distinctions
- Finding an indicator does not validate every inference about it.
- Identify the trust boundary and the party controlling each input.
- Use both positive and negative cases; document measurement limitations.

## Hands-on lab
Read `dns_triage.py` before running the following from this lab folder:

~~~bash
python3 dns_triage.py
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
