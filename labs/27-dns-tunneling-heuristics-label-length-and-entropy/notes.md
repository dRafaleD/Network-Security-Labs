# Day 27 — DNS Tunneling Heuristics: Label Length and Entropy

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **DNS Tunneling Heuristics: Label Length and Entropy** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. DNS tunnels pack data into long, high-entropy subdomain labels, so length and character randomness are first-pass signals.
2. Score each query name by label length and Shannon entropy, then aggregate per registered domain.
3. Content delivery networks and some security products also use long random labels, so allow-list known services.

## Important distinctions
- A single long name is weak evidence; many distinct long names under one domain is stronger.
- Thresholds must be tuned on your own traffic baseline.
- Encrypted DNS hides the names from this check entirely.

## Hands-on lab
Read `dns_tunnel_demo.py` before running the following from this lab folder:

~~~bash
python3 dns_tunnel_demo.py
~~~


## Assignments
1. Predict which domains are flagged as suspected tunnels.
2. Run the demo and record the entropy and label length for each domain.
3. Lower the entropy threshold and describe the new false positives.
4. Add an assertion that `www.example.test` is not flagged.
5. Describe how an attacker could keep labels short and low-entropy to evade the check.
6. Propose an independent signal, such as query volume per domain or TXT record usage.

## Knowledge check
1. Where does the input originate, and who controls it?
2. What was directly observed, as opposed to inferred?
3. What assumptions might fail in production?
4. Which evidence would be insufficient on its own?
5. What should an automated test check?

## Safety and limitations
Use only authorized systems and synthetic data. The example is not a complete security or detection product.
