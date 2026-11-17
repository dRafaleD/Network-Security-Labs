# Day 45 — Authenticated Sensor Provenance and Relay Deduplication

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](sensor_auth_demo.py)

## After Day 44
Day 44 grouped IPv6 observations by claimed **upstream sensor**, not by log collector. But a text label claiming `sensor-a` can be forged. Today's toy model adds **HMAC-authenticated producer records**.

Each fictional sensor has a different shared key. An event's HMAC covers its producer, event ID, IPv6 address, MAC and timestamp. A relay may copy a message, but the matching `(producer, event_id)` still denotes **one upstream observation**. The verifier rejects modified fields or unknown producers before counting origins.

## Important limits
- HMAC proves possession of the shared key **within this toy trust model**, not a human or physical device's identity.
- If a sensor key is compromised, an attacker can create validly tagged events.
- Distinct authenticated producer IDs do **not** guarantee independent underlying hardware or prove malicious IPv6 spoofing.
- Real systems need secure key provisioning, replay windows, key rotation and authoritative timestamps.

## Reproduce
~~~bash
python3 labs/45-authenticated-sensor-provenance-and-relay-deduplication/sensor_auth_demo.py
~~~

## Questions
1. Why are collector and original producer different identities?
2. Why include an event ID and timestamp in a signed record?
3. Why cannot HMAC alone prevent an attacker from replaying an old valid event?
4. How should a real system deal with a compromised sensor key?
5. Why do two accepted HMACs not prove an attack occurred?

## Safety
Only fictional IPv6 documentation addresses and in-memory objects. No network I/O.
