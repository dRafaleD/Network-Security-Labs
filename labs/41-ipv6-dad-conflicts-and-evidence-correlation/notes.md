# Day 41 — IPv6 DAD Conflicts and Evidence Correlation

[English](notes.md) · [Türkçe](notes.tr.md) · [Python practice](dad_conflicts_demo.py)

## Link to Day 40
Day 40 established that a changed IPv6 neighbor-cache entry requires corroboration. Day 41 examines **Duplicate Address Detection (DAD)** logs: a machine checking whether an IPv6 address is already used. A DAD failure may arise from a real address collision, a temporary observation, network configuration or hostile traffic. **It does not identify an attacker.**

## Evidence fields
A synthetic DAD event records candidate IPv6 address, locally observed MAC address, event type and offset-aware timestamp. A separate neighbor record contains an IPv6-to-MAC mapping and its observation time. This is *not* live Neighbor Discovery or a packet decoder.

The toy joins records only if they:
1. Belong to the documentation prefix `2001:db8:10::/64`.
2. Refer to the identical IPv6 address.
3. Show **different** MAC values.
4. Arrive within a five-second correlation window.

Outputs:
- **CORROBORATED_CONFLICT:** another MAC mapping exists near a DAD failure.
- **UNCONFIRMED:** a DAD failure has no nearby independent record.
- **NO_FAILURE:** a DAD success event is not a conflict.
- **OUT_OF_SCOPE / INVALID:** unsupported or malformed input.

This does not certify which physical host owns an address: randomized MACs, VM migration, bridge behavior, stale caches, clock skew and duplicate telemetry can mislead.

## Run without network access
~~~bash
python3 labs/41-ipv6-dad-conflicts-and-evidence-correlation/dad_conflicts_demo.py
~~~

## Exercises
1. Explain DAD and Neighbor Discovery in one sentence each.
2. Why can a stale neighbor entry produce a false correlation?
3. Which source besides a local cache could corroborate a reported conflict?
4. Why is a conflicting MAC not proof of spoofing?
5. How would clock skew affect the five-second window?

## Safety
No interfaces, packets, sockets or real hosts are used. Local synthetic records illustrate triage, not detection or attribution.
