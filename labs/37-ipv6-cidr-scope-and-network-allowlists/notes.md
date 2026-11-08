# Day 37 — IPv6 CIDR Scope and Network Allowlists

[English](notes.md) · [Türkçe](notes.tr.md) · [Python lab](ipv6_policy_demo.py)

## Why IPv6 changes security reviews
An organization may carefully configure IPv4 firewall rules while ignoring a second, IPv6-enabled path to the same service. IPv4 and IPv6 have **different address families**, so a policy for one is not automatically a policy for the other. A correct review inventories listening addresses and applies explicit policies for every enabled family.

## Address ranges and boundaries
An IPv6 CIDR such as `2001:db8:10::/64` describes an address **prefix and subnet**, not an authenticated person. `2001:db8::/32` is a documentation range; this lab uses it so examples cannot accidentally target a public server. IPv6 link-local addresses generally use `fe80::/10` and include interface/scope considerations; they should not be treated as globally reachable sources.

## Policy design
The lab defines an offline service allowlist: only TCP port 443 from a specified IPv6 training subnet. Everything else is denied by default, including IPv4 inputs. It **does not send packets** or modify any operating-system firewall.

```bash
python3 ipv6_policy_demo.py
```

## Reading the results
- An IPv6 source inside the allowed `/64` with TCP/443 should pass.
- An address from another `/64`, a link-local IPv6 address, or TCP/22 should fail.
- An IPv4 address should not match an IPv6 rule.

## Exercises
1. Predict the output before execution; explain each denial.
2. Change the source prefix from `/64` to `/48`; which additional addresses are covered?
3. Add a separate IPv4 allow rule, *without* weakening the IPv6 rule.
4. Explain why CIDR membership is **not** a substitute for identity-based authorization.
5. Identify provider-specific issues absent here: statefulness, routing, egress and dual-stack listeners.

## Safety and scope
Documentation addresses and Python standard library only. Real policies depend on your authorized environment and cloud/OS firewall implementation.
