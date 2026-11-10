# Day 39 — IPv6 Neighbor Discovery: NS, NA and DAD Triage

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline validation model](ndp_triage_demo.py)

## Continue from Router Advertisements
Day 38 studied **Router Advertisements (RA, ICMPv6 type 134)** and trust boundaries. Today we look at two other Neighbor Discovery Protocol messages:
- **Neighbor Solicitation (NS, type 135):** asks about an IPv6 neighbor or performs address checks.
- **Neighbor Advertisement (NA, type 136):** communicates information about an IPv6 neighbor.

Address ownership and link-layer neighbor mappings matter for local network reliability, but observing an NS/NA message does not identify the human or device that intended a change.

## Key rules and exceptions
- For authentic NDP messages, IPv6 **Hop Limit must be 255**. A value of 64 should fail protocol validation.
- NS/NA **target addresses must not be multicast addresses**.
- An NS with unspecified source address `::` can be legitimate **Duplicate Address Detection (DAD)**; such messages have special constraints (including absence of a Source Link-Layer Address option). Do not flag every `::` as an attack.
- An NA must not use the unspecified address as its source. If an NA is sent to a **multicast destination**, the Solicited flag must be clear.
- A syntactically plausible record can still be spoofed by an on-link actor. Actual trust also depends on switch protections, topology and independent telemetry.

## Practice (zero network I/O)
`ndp_triage_demo.py` reads **fabricated message dictionaries**, checks a short subset of structural rules, and labels them `CONSISTENT` or `REVIEW`. It models a normal NS, a DAD NS, an invalid DAD option, an NA with invalid Solicited flag, and an invalid Hop Limit.

```bash
python3 ndp_triage_demo.py
```

## Tasks
1. What is the functional difference between NS, NA and the previous day's RA?
2. Why is DAD an important exception to a simplistic `source_ip != ::` rule?
3. Explain why Hop Limit 255 limits off-link forgery but does not authenticate an on-link sender.
4. Add a valid NA to the fixture. Which flag constraints apply?
5. Which information from an authorized PCAP, switch port and neighbor table might corroborate a suspected spoofing event?
6. List the protocol checks missing from this deliberately limited model (options, checksums, destination rules, rate/context).

## Scope
The script **does not parse real packets** or implement the complete RFC 4861/4862 rules. It sends no ICMPv6 traffic, probes no hosts and modifies no network configuration. Use only authorized evidence when extending the lab.
