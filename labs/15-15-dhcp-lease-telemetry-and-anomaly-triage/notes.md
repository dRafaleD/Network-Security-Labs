# Day 15 — DHCP Lease Telemetry, Address Changes and Anomaly Triage

[English](notes.md) · [Türkçe](notes.tr.md)

## Goal
Understand dhcp lease telemetry, address changes and anomaly triage through a fully local, harmless experiment. Keep observation separate from inference.

## Core concepts
1. **DHCP discover/offer/request/ack** — document the boundary, expected behavior and limitations.
2. **lease lifetimes** — document the boundary, expected behavior and limitations.
3. **client identifiers and MAC addresses** — document the boundary, expected behavior and limitations.
4. **address reuse and legitimate churn** — document the boundary, expected behavior and limitations.
5. **rogue server detection concepts** — document the boundary, expected behavior and limitations.
6. **baseline and anomaly triage** — document the boundary, expected behavior and limitations.

## Procedure
The included `lease_triage.py` is a synthetic training example. From the lab directory:

```bash
python3 lease_triage.py
```

```bash
ip address show
```

```bash
ip route
```

**Expected:** Repeated MAC/IP offered by two server labels is flagged for review, not declared malicious.

## Observations to record
Write down the machine/tool versions, exact command, input, actual output, unexpected behavior, and interpretation. Explain which results are facts and which remain hypotheses.

## Exercises
1. Run the baseline and save the observed output.
2. Change one harmless input and predict what happens before running.
3. Add a negative test and distinguish a rejection from a failure to observe.
4. Restore the original, rerun it, and explain why regression tests matter.
5. Identify two realistic false-positive explanations.
6. Identify a useful independent corroborating observation.
7. Draft a short report stating limitations explicitly.

## Review questions
1. What does DHCP discover/offer/request/ack mean, why does it matter, and what does it not guarantee?
2. What does lease lifetimes mean, why does it matter, and what does it not guarantee?
3. What does client identifiers and MAC addresses mean, why does it matter, and what does it not guarantee?
4. What does address reuse and legitimate churn mean, why does it matter, and what does it not guarantee?
5. What does rogue server detection concepts mean, why does it matter, and what does it not guarantee?
6. What does baseline and anomaly triage mean, why does it matter, and what does it not guarantee?
7. What would improve the confidence of your result?
8. Which regression test should be automated first?

## Ethics and scope
Use only locally generated data and infrastructure you own or are authorized to study. Findings from an individual signal are not proof of an incident.
