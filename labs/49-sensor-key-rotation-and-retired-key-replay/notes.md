# Day 49 — Sensor Key Rotation and Retired-Key Replay

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline Python](rotation_replay_demo.py)

## After Day 48
Day 48 enrolled a new boot epoch using a one-time challenge. However, a compromised or retired sensor **key** must also stop authenticating new records—even when the record has a perfectly valid HMAC calculated using that old key.

## Toy policy
Each fictional IPv6 sensor observation binds producer, **key ID**, boot, sequence number, event time, type and address under HMAC. The verifier looks the key up in its own registry, checks authenticity, then separately checks the controller-maintained **currently active key**.

Before rotation, `key-1` is accepted and `key-2` is inactive. Following an application-controlled change, `key-1` is rejected despite correct HMAC, while new `key-2` observations work. Replay identity includes producer, key ID, boot and sequence; a timestamp freshness window provides another independent check.

## Run
```bash
python3 labs/49-sensor-key-rotation-and-retired-key-replay/rotation_replay_demo.py
```

## Questions
Why isn't a correct HMAC sufficient once a key is retired? Why must the key registry be application-controlled? Can a sender invent a new key ID to bypass authentication? What durable policy and replay data does a real collector need after restart?

## Limits
Exposed training keys, fictional addresses, in-memory controller. No packets, real cryptographic enrollment, live scanning or physical sensor attribution.
