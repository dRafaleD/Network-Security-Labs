#!/usr/bin/env python3
"""Synthetic IPv6 neighbor-cache reviews; no packet or interface access."""
from ipaddress import IPv6Address, IPv6Network

TRAINING_PREFIX = IPv6Network("2001:db8:10::/64")
BASELINE = {
    "2001:db8:10::20": {"mac": "02:00:5e:00:53:20", "switch_port": "port-7"}
}
VALID_STATES = {"REACHABLE", "STALE", "DELAY", "PROBE"}


def evaluate(record):
    try:
        address = IPv6Address(record["ipv6"])
    except (ValueError, TypeError, KeyError):
        return "INVALID", "bad IPv6 address"
    if address not in TRAINING_PREFIX:
        return "REVIEW", "address outside documented training prefix"
    if record.get("state") not in VALID_STATES:
        return "INVALID", "unknown simplified cache state"
    key = str(address)
    known = BASELINE.get(key)
    if known is None:
        return "NEW", "untracked neighbor; collect context"
    if record.get("mac", "").lower() != known["mac"]:
        return "REVIEW", "MAC mapping differs from baseline"
    if record.get("switch_port") != known["switch_port"]:
        return "REVIEW", "switch port differs from baseline"
    return "CONSISTENT", "matches baseline; cache state alone is not an attack"


def main():
    base = {"ipv6": "2001:db8:10::20", "mac": "02:00:5e:00:53:20",
            "switch_port": "port-7", "state": "REACHABLE"}
    cases = [
        ("normal", base, "CONSISTENT"),
        ("stale entry", {**base, "state": "STALE"}, "CONSISTENT"),
        ("MAC changed", {**base, "mac": "02:00:5e:00:53:99"}, "REVIEW"),
        ("port moved", {**base, "switch_port": "port-9"}, "REVIEW"),
        ("new neighbor", {**base, "ipv6": "2001:db8:10::99"}, "NEW"),
    ]
    for name, record, expected in cases:
        decision, reason = evaluate(record)
        print(f"{name:15} {decision:11} {reason}")
        assert decision == expected, (name, decision)
    print("All synthetic cases verified; no attribution performed.")


if __name__ == "__main__":
    main()
