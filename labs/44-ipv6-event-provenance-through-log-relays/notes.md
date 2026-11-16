# Day 44 — IPv6 Event Provenance Through Log Relays

[English](notes.md) · [Türkçe](notes.tr.md) · [Python practice](relay_provenance_demo.py)

## Continuing Day 43
Day 43 grouped apparently independent IPv6 conflict evidence by `origin`. In a real logging pipeline, **one sensor can forward the same observation to multiple collectors**. Distinct collector names are not distinct sources.

## Model
For a fictional IPv6 Duplicate Address Detection (DAD) failure, each correlated record carries:
- an **upstream** identifier for the originating sensor;
- a **collector** identifier for the system that received/forwarded it;
- IPv6 address, MAC, offset-free synthetic time and uncertainty.

The same event forwarded to east and west collectors counts as **ONE_ORIGIN**. A second fictional sensor adds a second origin, reported as **MULTI_ORIGIN**. Invalid/missing upstream labels are excluded rather than promoted to independent evidence.

The correlation first checks DAD_FAIL, exact IPv6 address, different MAC and a possible match within a five-second window accounting for uncertainty.

## Run
~~~bash
python3 labs/44-ipv6-event-provenance-through-log-relays/relay_provenance_demo.py
~~~

## Questions
1. Why is a log collector not always the original event producer?
2. How could forwarding and ingestion retries inflate counts?
3. What should happen when upstream provenance is missing or untrusted?
4. Why is `MULTI_ORIGIN` still not proof of independent hardware or spoofing?
5. What external telemetry could help corroborate these records?

## Scope
Only synthetic, documentation-range IPv6 addresses. No network interfaces or packets are accessed. Textual upstream IDs can be forged, so source independence remains a hypothesis.
