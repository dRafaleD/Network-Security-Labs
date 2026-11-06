# Day 35 — MAC Address OUI and Randomization Checks

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **MAC Address OUI and Randomization Checks** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. The first three bytes of a MAC address (the OUI) identify the vendor, and a lookup table can label devices.
2. The second-least-significant bit of the first byte marks a locally administered address, which is typical for randomized MACs.
3. A device that rotates its MAC looks like many devices, so inventories must account for it.

## Important distinctions
- A MAC address is easy to set by hand; treat it as a label, not as proof of identity.
- An unknown OUI can mean a new vendor or a randomized address.
- Use documentation-style addresses in lab examples.

## Hands-on lab
Read `mac_demo.py` before running the following from this lab folder:

~~~bash
python3 mac_demo.py
~~~


## Assignments
1. Predict which addresses are locally administered.
2. Run the demo and record the vendor label for each address.
3. Add a multicast address and check how the bit test treats it.
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
