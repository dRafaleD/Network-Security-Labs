# Day 29 — Subnet Membership and VLAN Policy Validation

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Subnet Membership and VLAN Policy Validation** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Each VLAN maps to one subnet; a host whose address falls outside it signals a misconfiguration or a spoofed address.
2. Use a real IP library instead of string prefixes, since `10.0.1.5` and `10.0.10.5` share a prefix.
3. Export the expected mapping from your source of truth and check it regularly.

## Important distinctions
- Static mapping tables go stale; the check finds drift, not intent.
- Hosts with several interfaces need one entry per interface.
- A passing check says nothing about firewall rules between VLANs.

## Hands-on lab
Read `vlan_demo.py` before running the following from this lab folder:

~~~bash
python3 vlan_demo.py
~~~


## Assignments
1. Predict which hosts violate the mapping.
2. Run the demo and record each violation.
3. Add a host with two interfaces in different VLANs.
4. Add an assertion for one security property.
5. Describe a negative case and a potential false positive.
6. Propose an independent corroboration method.

## Knowledge check
1. Where does the input originate, and who controls it?
2. What was directly observed, as opposed to inferred?
3. What assumptions might fail in production?
4. Which evidence would be insufficient on its own?
5. What should an automated test check?

## Safety and limitations
Use only authorized systems and synthetic data. The example is not a complete security or detection product.
