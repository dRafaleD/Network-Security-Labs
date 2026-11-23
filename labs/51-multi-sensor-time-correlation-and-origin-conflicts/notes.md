# Day 51 — Multi-Sensor Time Correlation and Origin Conflicts

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline Python](time_correlation_demo.py)

## After Day 50
Day 50 counted distinct sensor **origins** instead of duplicate relay deliveries. Day 51 considers an additional requirement: matching sensors should report compatible **event facts and times**.

## Model
The toy collector has application-controlled sensor/relay mappings and active membership. Each fictional IPv6 Duplicate Address Detection event carries a sensor ID, event type, documentation IPv6 address, timestamp and boot ID under toy HMAC.

The application deduplicates relayed observations by origin. Two independent sensors reporting the same event and address within a **two-second time window** yield `CORROBORATED_CONTEXT`. Incompatible types/addresses yield `CROSS_SENSOR_CONFLICT`; incompatible times yield `TIME_DISAGREEMENT`. Contradictory observations from a single sensor are flagged separately.

## Run
```bash
python3 labs/51-multi-sensor-time-correlation-and-origin-conflicts/time_correlation_demo.py
```

## Questions
Why must two observations match on event meaning, not only time? How can clock skew produce false disagreements? Why is a relay copy not independent corroboration? Can authentic HMAC messages still be factually false?

## Limits
Fictional, static key material and no real network traffic. HMAC and small timing windows do not independently authenticate sensor truthfulness or physical identity.
