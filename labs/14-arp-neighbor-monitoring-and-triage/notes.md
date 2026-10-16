# Day 14 — ARP Neighbor Monitoring and Layer-2 Triage

[English](notes.md) | [Türkçe](notes.tr.md)

## Objective

Build an authorized, local and repeatable practical exercise about arp neighbor monitoring and layer-2 triage. The lab intentionally uses harmless synthetic data. A tool observation is evidence of a particular execution, not proof of compromise.

## Connected concepts

1. **ARP basics** — identify its role, trust assumptions, and limitations in the workflow.
2. **IPv6 Neighbor Discovery** — identify its role, trust assumptions, and limitations in the workflow.
3. **IP/MAC baseline** — identify its role, trust assumptions, and limitations in the workflow.
4. **mapping anomalies** — identify its role, trust assumptions, and limitations in the workflow.
5. **false positives** — identify its role, trust assumptions, and limitations in the workflow.
6. **passive monitoring** — identify its role, trust assumptions, and limitations in the workflow.

## Setup and practice

Use the included `arp_triage.py` as the locally controlled target. Do not test unrelated infrastructure or real suspicious artifacts.

```bash
python3 arp_triage.py
```

```bash
ip neigh show
```

## Analysis workflow

1. Predict expected results before running the lab.
2. Collect actual outputs and note the tool/version/environment.
3. Separate observed facts from inferred explanations.
4. Introduce one harmless negative case, then rerun.
5. Explain whether a result could be a false positive, incomplete evidence, or a configuration issue.
6. Keep the original sample and record a checksum when preserving evidence.
7. Compare what static/configuration data says with the runtime observation.
8. Record a concise conclusion and at least one unresolved question.

## Mini challenges

- **Baseline:** run the provided example and write down exact output and assumptions.
- **Change one variable:** alter one benign marker, header, log field, or configuration setting, then record what changed.
- **Regression:** restore the original test and ensure that it still produces the expected observation.
- **Detection vs proof:** describe why your evidence does not by itself establish malicious activity.

## Review questions

1. What does ARP basics contribute, and what does it not guarantee?
2. What does IPv6 Neighbor Discovery contribute, and what does it not guarantee?
3. What does IP/MAC baseline contribute, and what does it not guarantee?
4. What does mapping anomalies contribute, and what does it not guarantee?
5. What does false positives contribute, and what does it not guarantee?
6. What does passive monitoring contribute, and what does it not guarantee?
7. What independent evidence would strengthen this conclusion?
8. How could you reproduce the result next week?

## Safety and interpretation

This educational example is isolated, local-only and synthetic. Never infer safety from a missing match or compromise from an isolated suspicious indicator.