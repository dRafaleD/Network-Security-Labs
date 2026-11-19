# Day 47 — Sensor Restarts, Boot Epochs and Sequence Reuse

[English](notes.md) · [Türkçe](notes.tr.md) · [Python practice](boot_epoch_demo.py)

## Day 46 follow-up
Day 46 rejected replayed sensor records by `(producer, sequence)` and a freshness window. But a legitimate sensor may **restart** and begin its sequence counter again at 1. Rejecting all repeated numbers forever would block newly produced events.

## Toy design
Each HMAC-protected event includes a **boot ID** along with producer, sequence, timestamp, event kind and IPv6 documentation address. A *trusted controller registry*, separate from the event, records which boot ID is currently active.

The replay identity becomes `(producer, boot ID, sequence)`. Events from the old boot are denied after a simulated authenticated enrollment; fresh events from the new boot can use sequence 1. The HMAC prevents unauthorized edits **assuming keys remain secret**.

## Run
```bash
python3 labs/47-sensor-restarts-boot-epochs-and-sequence-reuse/boot_epoch_demo.py
```

## Questions
1. Why does a counter reset not necessarily indicate malicious replay?
2. Why can't the verifier simply trust a new boot ID claimed by the event?
3. What makes enrollment and key rotation difficult in a distributed collector?
4. Why must duplicate-state survive a process restart in production?
5. Does a valid HMAC prove independent physical sensor provenance?

## Limits
In-memory trust registry, toy public keys and fake clock. No real sensor, network traffic or secure enrollment; HMAC is not sufficient if the key is compromised.
