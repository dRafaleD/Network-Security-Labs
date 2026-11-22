# Day 50 — Sensor Provenance after Key Rotation and Relay Fanout

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline Python](sensor_provenance_demo.py)

## After Day 49
A sensor's old HMAC key can be retired. Today we examine **corroboration**: a valid observation forwarded through multiple relays is still **one sensor's claim**, not independent evidence.

## Model
The fictional collector maintains its own map from relay endpoints to sensor identities and an application-controlled set of **active producers**. The record's producer field and HMAC are checked against that registry before counting evidence.

Two copies of sensor A's signed event are counted once. A matching independent sensor B can establish `CORROBORATED`; disagreement is marked `CROSS_SENSOR_CONFLICT`. Contradictory signed claims from one origin become `SENSOR_CONFLICT`. After sensor A is retired, its older messages no longer contribute even when they retain valid toy tags.

## Run
```bash
python3 labs/50-sensor-provenance-after-key-rotation-and-relay-fanout/sensor_provenance_demo.py
```

## Questions
Why is a relay not another independent sensor? What does a valid HMAC actually authenticate? Can two physical sensors share a compromised upstream controller? Why should retired keys and registrations be enforced by the collector rather than the event text?

## Limits
Fixed public toy keys and fictional documentation IPv6 address. No real packets, sensor enrollment, production clock or incident attribution.
