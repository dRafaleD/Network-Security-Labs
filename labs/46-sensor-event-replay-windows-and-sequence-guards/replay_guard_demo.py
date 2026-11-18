#!/usr/bin/env python3
"""Synthetic signed IPv6 sensor events with replay protection; no network I/O."""
from hashlib import sha256
import hmac
import json

KEYS = {"sensor-a": b"toy-key-a", "sensor-b": b"toy-key-b"}
SEEN: set[tuple[str, int]] = set()
WINDOW = 10

def tag(event: dict, key: bytes) -> str:
    text = json.dumps({k: event[k] for k in
                      ("producer", "sequence", "second", "address", "event")},
                      sort_keys=True, separators=(",", ":"))
    return hmac.new(key, text.encode(), sha256).hexdigest()

def make(producer: str, sequence: int, second: int, event: str = "DAD_FAIL") -> dict:
    data = {"producer": producer, "sequence": sequence,
            "second": second, "address": "2001:db8::20", "event": event}
    return {**data, "mac": tag(data, KEYS[producer])}

def review(record: dict, now: int) -> str:
    try:
        producer = record["producer"]
        key = KEYS.get(producer)
        sequence, observed = record["sequence"], record["second"]
        if not key or type(sequence) is not int or sequence < 1 or type(observed) is not int:
            return "INVALID_FIELDS"
        if not isinstance(record["mac"], str):
            return "BAD_TAG"
        if not hmac.compare_digest(tag(record, key), record["mac"]):
            return "BAD_TAG"
        if abs(now - observed) > WINDOW:
            return "OUTSIDE_WINDOW"
        identity = (producer, sequence)
        if identity in SEEN:
            return "REPLAY"
        SEEN.add(identity)
        return "ACCEPT"
    except (KeyError, TypeError, ValueError):
        return "INVALID_FIELDS"

def main():
    first = make("sensor-a", 10, 100)
    second = make("sensor-b", 10, 101)
    cases = [
        ("valid", first, 100, "ACCEPT"),
        ("identical replay", first, 101, "REPLAY"),
        ("different sensor same number", second, 101, "ACCEPT"),
        ("tampered address", {**first, "address": "2001:db8::99"}, 102, "BAD_TAG"),
        ("old signed event", make("sensor-a", 11, 50), 100, "OUTSIDE_WINDOW"),
        ("future signed event", make("sensor-a", 12, 120), 100, "OUTSIDE_WINDOW"),
        ("new sequence", make("sensor-a", 13, 103), 103, "ACCEPT"),
        ("sequence reused with fresh signature", make("sensor-a", 13, 104), 104, "REPLAY"),
        ("unknown producer", {**first, "producer": "unknown"}, 101, "INVALID_FIELDS"),
    ]
    for label, record, now, expected in cases:
        actual = review(record, now)
        assert actual == expected, (label, actual)
        print(f"{label:38} {actual}")
    print("9/9 synthetic sensor replay checks passed")

if __name__ == "__main__":
    main()
