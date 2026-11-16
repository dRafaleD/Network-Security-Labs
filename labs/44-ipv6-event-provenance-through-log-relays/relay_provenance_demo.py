#!/usr/bin/env python3
"""Synthetic DAD event correlation with upstream-source deduplication."""
from ipaddress import IPv6Address

DAD = {"ip": "2001:db8::20", "mac": "02:00:00:00:00:01",
       "time": 100, "uncertainty": 1, "kind": "DAD_FAIL"}
DIRECT = {
    "id": "r1", "collector": "collector-east", "upstream": "host-sensor-A",
    "ip": "2001:db8::20", "mac": "02:00:00:00:00:02",
    "time": 101, "uncertainty": 1,
}
FORWARDED = {**DIRECT, "id": "r2", "collector": "collector-west"}
INDEPENDENT = {**DIRECT, "id": "r3", "upstream": "switch-sensor-B",
               "collector": "collector-west", "time": 102}

def sources(event: dict, observations: list[dict], window: int = 5) -> set[str]:
    roots = set()
    for row in observations:
        try:
            if event["kind"] != "DAD_FAIL":
                continue
            if IPv6Address(event["ip"]) != IPv6Address(row["ip"]):
                continue
            if event["mac"].lower() == row["mac"].lower():
                continue
            if not isinstance(row["upstream"], str) or not row["upstream"].strip():
                continue
            if event["uncertainty"] < 0 or row["uncertainty"] < 0:
                continue
            gap = abs(event["time"] - row["time"])
            if max(0, gap - event["uncertainty"] - row["uncertainty"]) > window:
                continue
            roots.add(row["upstream"])
        except (KeyError, TypeError, ValueError):
            continue
    return roots

def status(event, rows):
    count = len(sources(event, rows))
    return "MULTI_ORIGIN" if count >= 2 else "ONE_ORIGIN" if count else "NONE"

def main():
    cases = [
        ("direct", DAD, [DIRECT], "ONE_ORIGIN"),
        ("two relay copies", DAD, [DIRECT, FORWARDED], "ONE_ORIGIN"),
        ("separate sensors", DAD, [DIRECT, FORWARDED, INDEPENDENT], "MULTI_ORIGIN"),
        ("missing upstream", DAD, [{**DIRECT, "upstream": ""}], "NONE"),
        ("different address", DAD, [{**DIRECT, "ip": "2001:db8::30"}], "NONE"),
        ("same MAC", DAD, [{**DIRECT, "mac": DAD["mac"]}], "NONE"),
        ("outside window", DAD, [{**DIRECT, "time": 150}], "NONE"),
        ("not DAD failure", {**DAD, "kind": "DAD_OK"}, [DIRECT], "NONE"),
    ]
    for label, event, rows, expected in cases:
        actual = status(event, rows)
        assert actual == expected, (label, actual)
        print(f"{label:22} {actual:13} source_roots={sorted(sources(event, rows))}")
    print("8/8 synthetic provenance scenarios passed; no packets transmitted")

if __name__ == "__main__":
    main()
