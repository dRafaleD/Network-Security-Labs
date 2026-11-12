#!/usr/bin/env python3
"""Read-only synthetic IPv6 Duplicate Address Detection evidence correlation."""
from datetime import datetime
from ipaddress import IPv6Address, IPv6Network

PREFIX = IPv6Network("2001:db8:10::/64")  # documentation-only addresses
WINDOW = 5
DAD_EVENTS = [
    {"id": "d1", "ip": "2001:db8:10::10", "mac": "02:00:5e:00:53:10",
     "event": "DAD_FAIL", "time": "2026-11-04T09:00:00+00:00"},
    {"id": "d2", "ip": "2001:db8:10::20", "mac": "02:00:5e:00:53:20",
     "event": "DAD_FAIL", "time": "2026-11-04T09:01:00+00:00"},
    {"id": "d3", "ip": "2001:db8:10::30", "mac": "02:00:5e:00:53:30",
     "event": "DAD_OK", "time": "2026-11-04T09:02:00+00:00"},
]
NEIGHBOR_OBSERVATIONS = [
    {"ip": "2001:db8:10::10", "mac": "02:00:5e:00:53:99",
     "time": "2026-11-04T09:00:02+00:00"},
    {"ip": "2001:db8:10::20", "mac": "02:00:5e:00:53:88",
     "time": "2026-11-04T09:01:20+00:00"},  # outside window
]

def review(event):
    try:
        address = IPv6Address(event["ip"])
    except (KeyError, TypeError, ValueError):
        return "INVALID"
    if address not in PREFIX:
        return "OUT_OF_SCOPE"
    if event.get("event") != "DAD_FAIL":
        return "NO_FAILURE"
    origin_time = datetime.fromisoformat(event["time"])
    candidates = [
        n for n in NEIGHBOR_OBSERVATIONS
        if IPv6Address(n["ip"]) == address
        and n["mac"].lower() != event["mac"].lower()
        and abs((datetime.fromisoformat(n["time"]) - origin_time).total_seconds()) <= WINDOW
    ]
    return "CORROBORATED_CONFLICT" if candidates else "UNCONFIRMED"

def main():
    expected = {"d1": "CORROBORATED_CONFLICT",
                "d2": "UNCONFIRMED", "d3": "NO_FAILURE"}
    for row in DAD_EVENTS:
        actual = review(row)
        assert actual == expected[row["id"]], (row["id"], actual)
        print(f"{row['id']}: {actual}")
    assert review({**DAD_EVENTS[0], "ip": "2001:db8:99::1"}) == "OUT_OF_SCOPE"
    assert review({**DAD_EVENTS[0], "ip": "not-an-ip"}) == "INVALID"
    print("5/5 synthetic triage checks passed; no network packets sent.")

if __name__ == "__main__":
    main()
