#!/usr/bin/env python3
"""Synthetic IPv6 sensor authentication; no packets, sockets, or real keys."""
from hashlib import sha256
import hmac
import json

KEYS = {
    "sensor-a": b"fictional-a-key",
    "sensor-b": b"fictional-b-key",
}
DAD_IP = "2001:db8::20"

def sign(event: dict, key: bytes) -> str:
    fields = {k: event[k] for k in ("event_id", "producer", "ip", "mac", "second")}
    body = json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(key, body, sha256).hexdigest()

def make(event_id: str, producer: str, mac: str, second: int) -> dict:
    event = {"event_id": event_id, "producer": producer, "ip": DAD_IP,
             "mac": mac, "second": second}
    event["tag"] = sign(event, KEYS[producer])
    return event

def verified(event: dict) -> bool:
    try:
        key = KEYS.get(event["producer"])
        if key is None or not isinstance(event["tag"], str):
            return False
        return hmac.compare_digest(sign(event, key), event["tag"])
    except (KeyError, TypeError, ValueError):
        return False

def producer_count(events: list[dict]) -> int:
    seen = set()
    origins = set()
    for event in events:
        if not verified(event):
            continue
        if event["ip"] != DAD_IP or abs(event["second"] - 100) > 5:
            continue
        identity = (event["producer"], event["event_id"])
        if identity in seen:
            continue
        seen.add(identity)
        origins.add(event["producer"])
    return len(origins)

def main() -> None:
    a = make("e-1", "sensor-a", "02:00:00:00:00:01", 100)
    b = make("e-2", "sensor-b", "02:00:00:00:00:02", 101)
    copied = dict(a)  # forwarded by another collector: same source event
    tampered = {**a, "mac": "02:00:00:00:00:99"}
    invented = {**a, "producer": "sensor-unknown"}
    late = make("e-3", "sensor-b", "02:00:00:00:00:03", 140)
    checks = [
        ("valid sensor A", verified(a)),
        ("valid sensor B", verified(b)),
        ("tampering rejected", not verified(tampered)),
        ("unknown producer rejected", not verified(invented)),
        ("relay copy counted once", producer_count([a, copied]) == 1),
        ("two different sensor origins", producer_count([a, copied, b]) == 2),
        ("late observation excluded", producer_count([late]) == 0),
        ("invalid tag excluded", producer_count([tampered]) == 0),
    ]
    for label, passed in checks:
        assert passed, label
        print(f"{label:31} PASS")
    print("8/8 synthetic provenance checks passed; no attribution inferred")

if __name__ == "__main__":
    main()
