# Day 43 — IPv6 Evidence Deduplication and Source Independence

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](evidence_dedup_demo.py)

## After Day 42
Timestamp uncertainty can make several log records appear related to one IPv6 Duplicate Address Detection (DAD) failure. But **two records are not necessarily two independent observations**: a forwarded log may duplicate an original event.

## Synthetic triage
The fixture matches IPv6 address, differing MAC value, a DAD failure and an uncertainty-adjusted five-second window. It then counts **unique observation origins**, not log rows:
- **NONE:** no compatible evidence.
- **SINGLE_SOURCE:** one origin (even if duplicated across records).
- **MULTI_SOURCE:** two distinct origins.

Distinct origin labels are **not proof of independence**; upstream sensors may share a feed, timestamps may be inaccurate and one malicious or faulty device can influence several logs. This is an educational evidence-quality marker, not an attacker classification.

## Reproduce
~~~bash
python3 labs/43-ipv6-evidence-deduplication-and-source-independence/evidence_dedup_demo.py
~~~

## Questions
1. Why does forwarding the same event to two log collectors not produce two independent pieces of evidence?
2. How could provenance metadata reveal that two sources are copies?
3. Which assumptions underlie the time-uncertainty match?
4. Why can multiple logs still fail to establish spoofing or actor identity?

## Safety
Uses documentation IPv6 space and fictional records. No sockets, packets or interfaces.
