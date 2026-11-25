# Day 53 — Practice Day: Offline Flow Log Triage

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](flow_triage.py)

Read 12 fictional flow summaries using RFC 5737 documentation networks. Validate addresses, protocol and counters before assigning traffic direction relative to the lab network. Aggregate bytes only for accepted nonempty records.

| Source / destination | Expected |
|---|---|
| Lab → lab | LAB_INTERNAL |
| Lab → peer | LAB_OUTBOUND |
| Peer → lab | LAB_INBOUND |
| Peer → peer | PEER_INTERNAL |
| Zero packets and bytes | EMPTY_FLOW |
| Negative bytes | INVALID_COUNTER |

**Exercises:** Classify the 12 rows by hand, compare byte totals, add a 60-byte valid inbound flow, and update the expected aggregate. Add a malformed address and confirm it is excluded. Explain why an outbound flow is not itself evidence of exfiltration.

Expected total for original data: internal 100, outbound 200, inbound 150, peer 80 bytes. No live traffic, network interfaces, scans or external endpoints. This is a data-quality exercise, not an IDS.

## Run
```bash
python3 labs/53-offline-flow-log-triage-practice/flow_triage.py
```
