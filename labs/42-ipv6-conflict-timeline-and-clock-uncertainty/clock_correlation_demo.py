#!/usr/bin/env python3
"""Synthetic IPv6 DAD timeline: time uncertainty changes confidence in a match."""
from ipaddress import IPv6Address

def correlate(dad: dict, neighbor: dict, window: int = 5) -> str:
    try:
        if IPv6Address(dad["ip"]) != IPv6Address(neighbor["ip"]):
            return "DIFFERENT_ADDRESS"
        if dad["mac"].lower() == neighbor["mac"].lower():
            return "SAME_MAC"
        if dad["kind"] != "DAD_FAIL":
            return "NOT_A_FAILURE"
        if min(dad["uncertainty"], neighbor["uncertainty"], window) < 0:
            return "INVALID_TIME"
        gap = abs(dad["second"] - neighbor["second"])
        error = dad["uncertainty"] + neighbor["uncertainty"]
        if gap + error <= window:
            return "DEFINITELY_NEAR"
        if max(0, gap - error) <= window:
            return "POSSIBLY_NEAR"
        return "OUTSIDE_WINDOW"
    except (KeyError, TypeError, ValueError):
        return "INVALID_RECORD"

def main():
    dad = {"ip": "2001:db8::20", "mac": "02:00:00:00:00:01",
           "kind": "DAD_FAIL", "second": 100, "uncertainty": 1}
    near = {"ip": "2001:db8::20", "mac": "02:00:00:00:00:02",
            "second": 102, "uncertainty": 1}
    cases = [
        ("strong", dad, near, "DEFINITELY_NEAR"),
        ("possible", dad, {**near, "second": 106}, "POSSIBLY_NEAR"),
        ("too late", dad, {**near, "second": 110}, "OUTSIDE_WINDOW"),
        ("other ip", dad, {**near, "ip": "2001:db8::99"}, "DIFFERENT_ADDRESS"),
        ("same mac", dad, {**near, "mac": dad["mac"]}, "SAME_MAC"),
        ("no failure", {**dad, "kind": "DAD_OK"}, near, "NOT_A_FAILURE"),
        ("negative error", dad, {**near, "uncertainty": -1}, "INVALID_TIME"),
        ("bad ip", dad, {**near, "ip": "invalid"}, "INVALID_RECORD"),
    ]
    for title, left, right, expected in cases:
        result = correlate(left, right)
        assert result == expected, (title, result)
        print(f"{title:16} {result}")
    print("8/8 uncertainty checks passed; no packet capture or attribution")

if __name__ == "__main__":
    main()
