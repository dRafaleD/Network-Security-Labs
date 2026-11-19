#!/usr/bin/env python3
"""Synthetic signed sensor events: boot epochs distinguish legitimate counter resets."""
import hashlib
import hmac
import json

KEYS = {"sensor-a": b"fictional-a-key"}
ACTIVE_BOOT = {"sensor-a": "boot-1"}  # Trusted controller state, not payload.
SEEN: set[tuple[str, str, int]] = set()

def authenticated_bytes(event: dict) -> bytes:
    fields = {k: event[k] for k in (
        "producer", "boot", "sequence", "event", "ipv6", "second")}
    return json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()

def issue(boot: str, seq: int, second: int) -> dict:
    fields = {
        "producer": "sensor-a", "boot": boot, "sequence": seq,
        "event": "DAD_FAIL", "ipv6": "2001:db8::20", "second": second
    }
    tag = hmac.new(KEYS["sensor-a"], authenticated_bytes(fields),
                   hashlib.sha256).hexdigest()
    return {**fields, "tag": tag}

def accept(event: dict, now: int) -> str:
    try:
        producer = event["producer"]
        key = KEYS.get(producer)
        if not key or type(event["sequence"]) is not int or event["sequence"] < 1:
            return "INVALID"
        if type(event["second"]) is not int or not isinstance(event["boot"], str):
            return "INVALID"
        if not isinstance(event["tag"], str):
            return "INVALID"
        expected = hmac.new(key, authenticated_bytes(event), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, event["tag"]):
            return "BAD_TAG"
        if event["boot"] != ACTIVE_BOOT.get(producer):
            return "OLD_OR_UNKNOWN_BOOT"
        if abs(now - event["second"]) > 10:
            return "OUTSIDE_WINDOW"
        identity = (producer, event["boot"], event["sequence"])
        if identity in SEEN:
            return "REPLAY"
        SEEN.add(identity)
        return "ACCEPT"
    except (KeyError, TypeError, ValueError):
        return "INVALID"

def main():
    old = issue("boot-1", 1, 100)
    tests = [
        ("first event", accept(old, 100), "ACCEPT"),
        ("same boot replay", accept(old, 101), "REPLAY"),
        ("next sequence", accept(issue("boot-1", 2, 102), 102), "ACCEPT"),
        ("forged boot field", accept({**old, "boot": "boot-2"}, 103), "BAD_TAG"),
    ]
    # Simulate externally authenticated device enrollment after restart.
    ACTIVE_BOOT["sensor-a"] = "boot-2"
    tests += [
        ("counter reset on new boot", accept(issue("boot-2", 1, 104), 104), "ACCEPT"),
        ("old boot remains rejected", accept(old, 105), "OLD_OR_UNKNOWN_BOOT"),
        ("new boot duplicate", accept(issue("boot-2", 1, 105), 105), "REPLAY"),
        ("new boot next counter", accept(issue("boot-2", 2, 106), 106), "ACCEPT"),
        ("expired event", accept(issue("boot-2", 3, 80), 106), "OUTSIDE_WINDOW"),
    ]
    for title, actual, expected in tests:
        assert actual == expected, (title, actual)
        print(f"{title:30} {actual}")
    print(f"{len(tests)}/{len(tests)} fictional sensor-restart checks passed")

if __name__ == "__main__":
    main()
