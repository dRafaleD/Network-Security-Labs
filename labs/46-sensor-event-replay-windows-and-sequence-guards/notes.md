# Day 46 — Sensor Event Replay Windows and Sequence Guards

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline Python](replay_guard_demo.py)

## Day 45 follow-up
Day 45 authenticated toy sensor records with HMAC and counted independent origins. But an attacker, faulty relay or ingestion retry can resend an **unaltered, validly tagged event**. A valid tag alone does not establish freshness.

## Defenses in the toy
An application-managed trusted key registry authenticates producer, sequence, timestamp, IPv6 documentation address and event type. The verifier then checks:
1. The HMAC tag matches.
2. The event timestamp is within a fictional ±10-second **freshness window**.
3. The `(producer, sequence)` tuple has not been observed before.

The model recognizes a duplicate, a different sensor with the same sequence, tampered data, stale/future timestamps, and a reused sequence with a newly computed valid tag. The replay cache is **volatile** and therefore not adequate across restarts.

## Run
~~~bash
python3 labs/46-sensor-event-replay-windows-and-sequence-guards/replay_guard_demo.py
~~~

## Questions
Why can't HMAC alone detect valid replay? What does clock skew do to a narrow window? What happens to deduplication state after a collector restart? How should keys and sequences be rotated without accepting old events?

## Limits
No traffic, sockets, interfaces or real secrets. Replay protection, source provenance and malicious attribution require additional controls in a production pipeline.
