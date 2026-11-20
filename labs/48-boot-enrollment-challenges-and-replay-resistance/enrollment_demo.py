#!/usr/bin/env python3
"""Offline sensor boot enrollment with a one-time challenge; no network IO."""
from hashlib import sha256
import hmac
import json

KEY = b"fictional-sensor-key"
ACTIVE_BOOT = {"sensor-a": "boot-1"}
CHALLENGES = {"sensor-a": {"nonce": "challenge-77", "expires": 120, "used": False}}
SEEN = set()

def signed(fields: dict) -> str:
    raw = json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(KEY, raw, sha256).hexdigest()

def enrollment_proof(producer: str, boot: str, nonce: str) -> str:
    return signed({"type":"enroll","producer":producer,"boot":boot,"nonce":nonce})

def enroll(producer: str, boot: str, nonce: str, proof: str, now: int) -> str:
    challenge = CHALLENGES.get(producer)
    if not challenge or challenge["used"] or now >= challenge["expires"]:
        return "NO_ACTIVE_CHALLENGE"
    if nonce != challenge["nonce"] or not isinstance(proof, str):
        return "INVALID_CHALLENGE"
    if not hmac.compare_digest(proof, enrollment_proof(producer, boot, nonce)):
        return "BAD_PROOF"
    if boot == ACTIVE_BOOT.get(producer):
        return "SAME_BOOT"
    challenge["used"] = True
    ACTIVE_BOOT[producer] = boot
    return "ENROLLED"

def event(producer: str, boot: str, seq: int) -> dict:
    fields = {"type":"event","producer":producer,"boot":boot,
              "sequence":seq,"ipv6":"2001:db8::20"}
    return {**fields, "tag":signed(fields)}

def verify(message: dict) -> str:
    try:
        if message["producer"] != "sensor-a" or type(message["sequence"]) is not int or message["sequence"] < 1:
            return "INVALID"
        fields = {k: message[k] for k in ("type","producer","boot","sequence","ipv6")}
        if not isinstance(message["tag"], str) or not hmac.compare_digest(message["tag"], signed(fields)):
            return "BAD_TAG"
        if message["boot"] != ACTIVE_BOOT["sensor-a"]:
            return "OLD_BOOT"
        identity = (message["producer"], message["boot"], message["sequence"])
        if identity in SEEN:
            return "REPLAY"
        SEEN.add(identity)
        return "ACCEPT"
    except (KeyError, TypeError, ValueError):
        return "INVALID"

def main():
    old = event("sensor-a","boot-1",1)
    cases = []
    cases.append(("old boot initially valid", verify(old), "ACCEPT"))
    cases.append(("old duplicate", verify(old), "REPLAY"))
    wrong = enrollment_proof("sensor-a","boot-2","wrong")
    cases.append(("wrong nonce", enroll("sensor-a","boot-2","wrong",wrong,100), "INVALID_CHALLENGE"))
    good = enrollment_proof("sensor-a","boot-2","challenge-77")
    cases.append(("valid enrollment", enroll("sensor-a","boot-2","challenge-77",good,101), "ENROLLED"))
    cases.append(("challenge reused", enroll("sensor-a","boot-3","challenge-77",good,102), "NO_ACTIVE_CHALLENGE"))
    cases.append(("old boot rejected", verify(event("sensor-a","boot-1",2)), "OLD_BOOT"))
    cases.append(("fresh boot can restart counter", verify(event("sensor-a","boot-2",1)), "ACCEPT"))
    cases.append(("fresh boot duplicate", verify(event("sensor-a","boot-2",1)), "REPLAY"))
    cases.append(("forged event", verify({**event("sensor-a","boot-2",2),"boot":"boot-3"}), "BAD_TAG"))
    for title, actual, expected in cases:
        assert actual == expected, (title, actual)
        print(f"{title:34} {actual}")
    print(f"{len(cases)}/{len(cases)} fictional enrollment checks passed")

if __name__ == "__main__":
    main()
