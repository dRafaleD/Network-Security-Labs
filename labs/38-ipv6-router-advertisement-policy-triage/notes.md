# Day 38 — IPv6 Router Advertisements and Trust Boundaries

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline lab](ra_guard_demo.py)

## From IP allowlists to local network trust
Day 37 checked IPv6 source addresses against an application policy. IPv6 hosts also learn network settings through **Neighbor Discovery Protocol (NDP)** and **Router Advertisements (RA)**. An RA can influence a host's default router and prefix configuration. An unexpected RA deserves investigation, but a single unexpected field is not proof of a hostile actor.

## Facts to keep separate
- RAs are ICMPv6 **type 134** and are normally sent from a **link-local IPv6 source**.
- Neighbor Discovery messages must arrive with an IPv6 **Hop Limit of 255**. This protects against off-link forwarding, not against a malicious on-link sender.
- A known link-local address or source MAC is an **indicator**, not cryptographic authentication; on-link attackers may spoof them.
- Router Advertisement Guard and switch-port policy can reduce exposure when configured correctly. Endpoint configuration and topology matter.
- A prefix such as `2001:db8:10::/64` in this lab is documentation-only. Prefix agreement does not prove router legitimacy.

## Offline decision model
`ra_guard_demo.py` checks a fabricated list of RA-like records against a known training segment, expected source/MAC, Hop Limit and advertised prefix. It returns **allow for this policy** or **review**, never sends a packet or changes a real router. The inputs are simplified dictionaries, not authentic packet captures.

```bash
python3 ra_guard_demo.py
```
Expected: the baseline matches; an unknown router, changed prefix, and invalid Hop Limit require review. Assertions guard the exercise outcomes.

## Exercises
1. Draw the trust boundary between the network, switch, and host.
2. Why does Hop Limit 255 not authenticate the source?
3. What changes if a legitimate router is replaced and its MAC address changes?
4. Add an allowed backup router to the policy, documenting the change.
5. Explain what evidence (switch port, authenticated configuration, packet capture, host route changes) might support a stronger conclusion.
6. Why could an allowed RA still be malicious if source properties were spoofed?

## Scope
No scanning, injection, live IPv6 packet crafting or actual RA Guard configuration. Production NDP parsing must enforce RFC details and avoid simplistic static identities as its only defense.
