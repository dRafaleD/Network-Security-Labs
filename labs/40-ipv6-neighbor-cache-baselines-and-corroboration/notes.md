# Day 40 — IPv6 Neighbor Cache Baselines and Corroboration

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline Python model](neighbor_cache_demo.py)

## From messages to operational context
Day 39 studied the **structure** of IPv6 Neighbor Solicitation and Neighbor Advertisement messages. This day focuses on **the changes an observer sees in a host's neighbor cache**. A neighbor cache maps IPv6 addresses to link-layer neighbors and maintains states such as REACHABLE or STALE.

A new MAC mapping or port change can be relevant to a local-network investigation. But cache contents are **observations**, not cryptographic identities. Legitimate devices, interface changes, virtual machines, switches and maintenance can all change the picture.

## Three dimensions to review
1. **Address scope:** the lab uses only documentation-range 2001:db8::/32 addresses. A new IPv6 address is not an attacker identifier.
2. **Layer-2 association:** a MAC address and switch port may support a correlation, but both can be transient or affected by spoofing/topology changes.
3. **Cache state:** STALE means the mapping has not been recently confirmed; it does **not** mean malicious or compromised.

Always distinguish **consistent with baseline**, **new and unreviewed**, and **changed mapping requiring investigation**. Do not collapse these into a malware/attack verdict.

## Run (no live packets)
~~~bash
python3 neighbor_cache_demo.py
~~~

The fixture includes a baseline mapping, the same neighbor becoming STALE, an unexpected MAC, a port move, and a previously unseen address. The program emits short review labels and assert-checks the decisions. It never reads your actual neighbor table, sends NS/NA packets, or changes your network configuration.

## Exercises
1. Describe how a learned neighbor table differs from an authenticated inventory.
2. Why can a STALE entry be normal?
3. Which benign explanations could produce a port move or changed MAC?
4. Add a planned maintenance exception and state how its expiration would work.
5. Name independent evidence: authorized PCAP, NDP flags, switch MAC table, DHCPv6/SLAAC context, host interface history and maintenance ticket.
6. How might an on-link spoofer defeat a simple static source-MAC comparison?

## Limits
This deterministic policy check does **not** parse NDP or establish that spoofing happened. Production detection needs topology-aware baselines, time synchronization, device identity, switch protections and an explicit investigation workflow.
