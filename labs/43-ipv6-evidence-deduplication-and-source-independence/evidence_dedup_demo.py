#!/usr/bin/env python3
"""Synthetic IPv6 conflict evidence: duplicate records are not independent sources."""
from ipaddress import IPv6Address

DAD = {"ip": "2001:db8::20", "mac": "02:00:00:00:00:01",
       "time": 100, "uncertainty": 1, "event": "DAD_FAIL"}
A = {"id": "a1", "origin": "host-telemetry", "ip": "2001:db8::20",
     "mac": "02:00:00:00:00:02", "time": 101, "uncertainty": 1}
DUPLICATE_A = {**A, "id": "a1-copy"}  # Forwarded copy of same observation.
B = {"id": "b1", "origin": "switch-log", "ip": "2001:db8::20",
     "mac": "02:00:00:00:00:03", "time": 103, "uncertainty": 1}

def evidence_sources(event: dict, records: list[dict], window: int = 5) -> set[str]:
    sources = set()
    for row in records:
        try:
            if event["event"] != "DAD_FAIL":
                continue
            if IPv6Address(row["ip"]) != IPv6Address(event["ip"]):
                continue
            if row["mac"].lower() == event["mac"].lower():
                continue
            uncertainty = row["uncertainty"] + event["uncertainty"]
            if min(row["uncertainty"], event["uncertainty"]) < 0:
                continue
            earliest_gap = max(0, abs(row["time"] - event["time"]) - uncertainty)
            if earliest_gap > window:
                continue
            sources.add(row["origin"])
        except (KeyError, TypeError, ValueError):
            continue
    return sources

def assess(event: dict, records: list[dict]) -> str:
    n = len(evidence_sources(event, records))
    return "MULTI_SOURCE" if n >= 2 else "SINGLE_SOURCE" if n == 1 else "NONE"

def main():
    cases = [
        ("one observation", DAD, [A], "SINGLE_SOURCE"),
        ("copied duplicate", DAD, [A, DUPLICATE_A], "SINGLE_SOURCE"),
        ("second origin", DAD, [A, DUPLICATE_A, B], "MULTI_SOURCE"),
        ("different address", DAD, [{**B, "ip": "2001:db8::99"}], "NONE"),
        ("same MAC", DAD, [{**B, "mac": DAD["mac"]}], "NONE"),
        ("late", DAD, [{**B, "time": 150}], "NONE"),
        ("no failure", {**DAD, "event": "DAD_OK"}, [A, B], "NONE"),
    ]
    for title, event, records, expected in cases:
        result = assess(event, records)
        assert result == expected, (title, result)
        print(f"{title:18} {result}")
    print("7/7 synthetic deduplication checks passed; no network traffic")

if __name__ == "__main__":
    main()
