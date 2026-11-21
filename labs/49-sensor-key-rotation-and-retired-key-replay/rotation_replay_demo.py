#!/usr/bin/env python3
"""Synthetic sensor key rotation and replay: no sockets or real credentials."""
from hashlib import sha256
import hmac
import json

KEYS = {"key-1": b"public-demo-key-one", "key-2": b"public-demo-key-two"}
ACTIVE_KEY = {"sensor-a": "key-1"}  # Set by a trusted controller, not events.
SEEN: set[tuple[str, str, str, int]] = set()

def canonical(fields: dict) -> bytes:
    return json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()

def issue(key_id: str, boot: str, sequence: int, second: int) -> dict:
    fields = {"producer": "sensor-a", "key_id": key_id, "boot": boot,
              "sequence": sequence, "second": second,
              "event": "DAD_FAIL", "ipv6": "2001:db8::20"}
    tag = hmac.new(KEYS[key_id], canonical(fields), sha256).hexdigest()
    return {**fields, "tag": tag}

def verify(event: dict, now: int) -> str:
    try:
        fields = {k: event[k] for k in
                  ("producer", "key_id", "boot", "sequence", "second", "event", "ipv6")}
        producer, key_id = fields["producer"], fields["key_id"]
        if not isinstance(producer, str) or not isinstance(key_id, str):
            return "INVALID"
        if type(fields["sequence"]) is not int or fields["sequence"] < 1:
            return "INVALID"
        if type(fields["second"]) is not int or not isinstance(fields["boot"], str):
            return "INVALID"
        key = KEYS.get(key_id)
        if key is None:
            return "UNKNOWN_KEY"
        if not isinstance(event["tag"], str):
            return "BAD_TAG"
        expected = hmac.new(key, canonical(fields), sha256).hexdigest()
        if not hmac.compare_digest(event["tag"], expected):
            return "BAD_TAG"
        if key_id != ACTIVE_KEY.get(producer):
            return "RETIRED_OR_INACTIVE_KEY"
        if abs(now - fields["second"]) > 10:
            return "OUTSIDE_WINDOW"
        identity = (producer, key_id, fields["boot"], fields["sequence"])
        if identity in SEEN:
            return "REPLAY"
        SEEN.add(identity)
        return "ACCEPT"
    except (KeyError, TypeError, ValueError):
        return "INVALID"

def main():
    old = issue("key-1", "boot-a", 1, 100)
    fresh = issue("key-2", "boot-b", 1, 105)
    checks = [
        ("original active key", verify(old, 100), "ACCEPT"),
        ("duplicate original event", verify(old, 101), "REPLAY"),
        ("new key not yet enrolled", verify(fresh, 105), "RETIRED_OR_INACTIVE_KEY"),
    ]
    # Models an authenticated controller policy change outside event data.
    ACTIVE_KEY["sensor-a"] = "key-2"
    checks.extend([
        ("retired old event", verify(issue("key-1", "boot-a", 2, 105), 105), "RETIRED_OR_INACTIVE_KEY"),
        ("new key first event", verify(fresh, 105), "ACCEPT"),
        ("new key duplicate", verify(fresh, 106), "REPLAY"),
        ("new key next sequence", verify(issue("key-2", "boot-b", 2, 106), 106), "ACCEPT"),
        ("valid but expired", verify(issue("key-2", "boot-b", 3, 80), 106), "OUTSIDE_WINDOW"),
        ("changed signed address", verify({**issue("key-2", "boot-b", 4, 107), "ipv6": "2001:db8::99"}, 107), "BAD_TAG"),
        ("unknown signer label", verify({**fresh, "key_id": "unknown"}, 105), "UNKNOWN_KEY"),
    ])
    for label, actual, expected in checks:
        assert actual == expected, (label, actual)
        print(f"{label:30} {actual}")
    print(f"{len(checks)}/{len(checks)} synthetic key-rotation checks passed")

if __name__ == "__main__":
    main()
