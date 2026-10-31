# Day 33 — TLS Version and Cipher Policy Audit

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **TLS Version and Cipher Policy Audit** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Allow TLS 1.2 and 1.3; reject SSLv3, TLS 1.0 and 1.1.
2. Reject weak ciphers such as RC4, 3DES and export-grade suites, and prefer forward secrecy.
3. Audit what each endpoint actually offers, not only the documentation.

## Important distinctions
- Supporting an old version is a risk only if clients can be downgraded to it.
- A policy audit does not validate certificates or hostnames.
- Legacy clients may need a documented exception with an expiry date.

## Hands-on lab
Read `tls_policy_demo.py` before running the following from this lab folder:

~~~bash
python3 tls_policy_demo.py
~~~


## Assignments
1. Predict which endpoints fail the policy.
2. Run the demo and record the reasons.
3. Add an exception with an expiry date and show that it is honored.
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
