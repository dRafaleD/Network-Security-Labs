# Day 36 — DNS Response TTL and Cache Expiry Correlation

[English](notes.md) · [Türkçe](notes.tr.md) · [Practice](dns_ttl_demo.py)

## Learning objective

Learn the trust and evidence boundaries of **DNS Response TTL and Cache Expiry Correlation** using harmless local fixtures.

## Core concepts

1. DNS TTL indicates how long a response may be cached, but actual resolver policy and validation can modify behavior.

2. An expired answer is not necessarily evidence of tampering; compare timestamps and cache state before making security claims.

3. Network event correlation needs monotonic or properly normalized timestamps and source provenance.

## Safe hands-on

Read the code and predict its output before running:

```bash
python dns_ttl_demo.py
```

Output is synthetic; no operations are sent to a live target.

## Assignments

1. Identify input provenance and untrusted fields.
2. Add and test a negative or boundary case.
3. Separate direct observations from interpretations.
4. Describe additional validation needed in a real environment.

## Knowledge check

- Is any single indicator sufficient?
- What can cause false positives or missing evidence?
- What inputs are needed to reproduce the result?

## Safety and limitations

No live malware, cloud accounts, system modifications, or outbound traffic. This minimal model is not an exact platform implementation.
