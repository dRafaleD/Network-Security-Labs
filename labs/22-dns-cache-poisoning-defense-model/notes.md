# Day 22 — DNS Cache Trust Boundaries and Poisoning Defenses

[English](notes.md) · [Türkçe](notes.tr.md)

## Goal
Understand why DNS answers need validation and how cache scope, TTL and source trust affect safe resolution. Work entirely with synthetic DNS-like records.

## Concepts
- DNS translates domain names into records; caches reduce lookup cost but can retain incorrect data.
- Source validation (matching the intended request/response context), TTL limits and DNSSEC validation are distinct mechanisms.
- DNSSEC authenticates signed DNS data when correctly validated; it does not encrypt DNS or guarantee a destination is safe.
- DNS over HTTPS/TLS protects the transport path, not the correctness of a malicious authoritative answer.
- Negative caching and expiry matter during incident response.

## Hands-on
```bash
python3 dns_cache_demo.py
```
Inspect the offline events. The demo enforces an expected question name, a validated flag supplied by a *simulated* upstream, and a maximum TTL; it is **not** a DNSSEC implementation.

## Questions
1. Which records should be cached and for how long?
2. What happens when an unvalidated answer claims a long TTL?
3. Why is encrypted DNS insufficient by itself?
4. How can stale cache entries affect an investigation?
5. What telemetry would a real resolver need?

## Safety
No network calls, no attacks on DNS servers, no packet spoofing.
