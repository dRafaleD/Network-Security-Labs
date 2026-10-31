# Day 30 — Beaconing Regularity and Jitter Analysis

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Beaconing Regularity and Jitter Analysis** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Automated check-ins repeat at nearly fixed intervals, while human browsing is irregular.
2. The coefficient of variation (standard deviation divided by the mean) of the gaps measures regularity.
3. Attackers add jitter, so combine regularity with destination rarity and byte sizes.

## Important distinctions
- Software updaters, mail clients and monitoring agents are also regular.
- Few samples give unreliable statistics; require a minimum count.
- A low variation is a lead, not proof of malicious activity.

## Hands-on lab
Read `beacon_demo.py` before running the following from this lab folder:

~~~bash
python3 beacon_demo.py
~~~


## Assignments
1. Predict which series is flagged.
2. Run the demo and record the variation of each series.
3. Add 30% jitter to the regular series and see whether it is still flagged.
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
