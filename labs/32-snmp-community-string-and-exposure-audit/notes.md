# Day 32 — SNMP Community String and Exposure Audit

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **SNMP Community String and Exposure Audit** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. SNMP v1 and v2c authenticate with a plain community string; defaults such as `public` and `private` are well known.
2. Prefer SNMPv3 with authentication and encryption, and restrict who can reach the service.
3. Audit device configs for defaults, write access and wide source ranges.

## Important distinctions
- Read-only access still leaks the network layout.
- A strong community string is still sent in clear text with v2c.
- An audit of configuration does not show whether the port is reachable; verify both.

## Hands-on lab
Read `snmp_audit_demo.py` before running the following from this lab folder:

~~~bash
python3 snmp_audit_demo.py
~~~


## Assignments
1. Predict which devices have findings.
2. Run the demo and record each finding.
3. Add a v3 device and confirm it produces no findings.
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
