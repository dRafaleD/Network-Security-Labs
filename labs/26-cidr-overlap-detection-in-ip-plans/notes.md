# Day 26 — CIDR Overlap Detection in IP Plans

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **CIDR Overlap Detection in IP Plans** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Two CIDR blocks overlap when one contains any address of the other.
2. Accidental overlap breaks routing and makes firewall rules ambiguous.
3. Intentional sub-allocation should be documented rather than silently accepted.

## Important distinctions
- Finding an indicator does not validate every inference about it.
- Identify the trust boundary and the party controlling each input.
- Use both positive and negative cases; document measurement limitations.

## Hands-on lab
Read `overlap_demo.py` before running the following from this lab folder:

~~~bash
python3 overlap_demo.py
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
