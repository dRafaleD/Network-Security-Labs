# Day 48 — Boot Enrollment Challenges and Replay Resistance

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](enrollment_demo.py)

## After Day 47
A sensor's sequence counter can legitimately restart at 1 after reboot. Day 47 bound records to a boot epoch, but **who authorizes a new boot ID?** Accepting one just because the sensor payload claims it would undermine anti-replay checks.

## Model
A fictional controller holds an active boot ID and issues a **one-time challenge nonce** with expiry. A sensor must return an HMAC covering the producer, proposed boot ID and nonce. After verification, the controller marks the challenge as used and updates its independent active-boot registry.

Event verification checks the HMAC, active boot and `(producer, boot, sequence)` replay key. This rejects old-boot events and repeated events while allowing sequence 1 in the newly enrolled boot.

## Run
```bash
python3 labs/48-boot-enrollment-challenges-and-replay-resistance/enrollment_demo.py
```

## Questions
1. Why is a boot ID inside the signed event insufficient to authorize its own enrollment?
2. Why should enrollment use an unpredictable, single-use challenge?
3. What happens when the controller restarts and loses replay state?
4. Why must device keys be protected and rotated?
5. Why is an HMAC-valid event not proof of physical sensor independence?

## Limits
All keys and nonces are fixed **toy values**; real challenges must be unpredictable and stored durably with secure lifecycle management. No packets, sockets or genuine telemetry.
