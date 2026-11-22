#!/usr/bin/env python3
"""Synthetic sensor quorum: signing key and relay paths do not create independence."""
from hashlib import sha256
import hmac
import json

KEYS = {"sensor-a": b"fictional-key-a", "sensor-b": b"fictional-key-b"}
ACTIVE = {"sensor-a", "sensor-b"}
COLLECTOR_ORIGIN = {
    "direct-a": "sensor-a",
    "relay-a": "sensor-a",
    "direct-b": "sensor-b",
}

def payload_bytes(fields: dict) -> bytes:
    return json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()

def issue(producer: str, status: str = "DAD_FAIL") -> dict:
    fields = {"producer": producer, "event_id": "evt-7",
              "ipv6": "2001:db8::7", "status": status, "boot": "boot-2"}
    key = KEYS[producer]
    return {**fields, "tag": hmac.new(key, payload_bytes(fields), sha256).hexdigest()}

def verified(collector: str, record: dict) -> bool:
    origin = COLLECTOR_ORIGIN.get(collector)
    if not origin or origin not in ACTIVE or not isinstance(record, dict):
        return False
    try:
        fields = {k: record[k] for k in (
            "producer", "event_id", "ipv6", "status", "boot")}
        tag = record["tag"]
        if fields["producer"] != origin or not isinstance(tag, str):
            return False
        expected = hmac.new(KEYS[origin], payload_bytes(fields), sha256).hexdigest()
        return hmac.compare_digest(expected, tag)
    except (KeyError, TypeError, ValueError):
        return False

def assess(observations: list[tuple[str, dict]]) -> str:
    by_sensor: dict[str, set[str]] = {}
    for collector, record in observations:
        if not verified(collector, record):
            continue
        if record["event_id"] != "evt-7":
            continue
        sensor = COLLECTOR_ORIGIN[collector]
        by_sensor.setdefault(sensor, set()).add(record["status"])
    if not by_sensor:
        return "NO_TRUSTED_EVIDENCE"
    if any(len(v) > 1 for v in by_sensor.values()):
        return "SENSOR_CONFLICT"
    if len({next(iter(v)) for v in by_sensor.values()}) > 1:
        return "CROSS_SENSOR_CONFLICT"
    return "CORROBORATED" if len(by_sensor) >= 2 else "SINGLE_SENSOR"

def main():
    a, b = issue("sensor-a"), issue("sensor-b")
    bad = {**a, "status": "OK"}
    cases = [
        ("one sensor", [("direct-a", a)], "SINGLE_SENSOR"),
        ("same sensor two relays", [("direct-a", a), ("relay-a", a)], "SINGLE_SENSOR"),
        ("two authenticated sensors", [("direct-a", a), ("direct-b", b)], "CORROBORATED"),
        ("conflicting sensor statuses", [("direct-a", a), ("direct-b", issue("sensor-b", "OK"))], "CROSS_SENSOR_CONFLICT"),
        ("same source contradicts itself", [("direct-a", a), ("relay-a", issue("sensor-a", "OK"))], "SENSOR_CONFLICT"),
        ("tampered signed record", [("direct-a", bad)], "NO_TRUSTED_EVIDENCE"),
        ("unregistered relay", [("unknown", a)], "NO_TRUSTED_EVIDENCE"),
    ]
    for name, observations, expected in cases:
        actual = assess(observations)
        assert actual == expected, (name, actual)
        print(f"{name:35} {actual}")
    ACTIVE.remove("sensor-a")  # Application-controlled retirement.
    assert assess([("direct-a", a), ("direct-b", b)]) == "SINGLE_SENSOR"
    assert assess([("direct-a", a)]) == "NO_TRUSTED_EVIDENCE"
    print("9/9 fictional sensor provenance checks passed")

if __name__ == "__main__":
    main()
