#!/usr/bin/env python3
"""Offline IPv6 NDP structural triage using fabricated records only."""
from ipaddress import IPv6Address


def review(record: dict) -> tuple[bool, str]:
    kind = record.get("icmpv6_type")
    if kind not in (135, 136):
        return False, "not an NS/NA message"
    if record.get("hop_limit") != 255:
        return False, "NDP Hop Limit must be 255"
    try:
        source = IPv6Address(record["source_ip"])
        target = IPv6Address(record["target_ip"])
    except (KeyError, ValueError, TypeError):
        return False, "invalid IPv6 address fields"
    if target.is_multicast or target.is_unspecified:
        return False, "invalid NS/NA target address"
    if kind == 135:
        if source.is_unspecified:
            if record.get("has_source_lladdr", False):
                return False, "DAD NS cannot include source link-layer address"
            if not record.get("destination_multicast"):
                return False, "DAD NS should use solicited-node multicast"
            return True, "DAD-like NS; further RFC checks required"
        return True, "NS structure consistent; sender is not authenticated"

    # Neighbor Advertisements (136)
    if source.is_unspecified:
        return False, "NA source cannot be unspecified"
    if record.get("destination_multicast") and record.get("solicited_flag"):
        return False, "multicast NA cannot set Solicited flag"
    return True, "NA structure consistent; sender is not authenticated"


def main():
    ns = {
        "icmpv6_type": 135, "hop_limit": 255,
        "source_ip": "fe80::10", "target_ip": "2001:db8:10::20",
        "has_source_lladdr": True, "destination_multicast": True,
        "solicited_flag": False
    }
    na = {
        "icmpv6_type": 136, "hop_limit": 255,
        "source_ip": "fe80::20", "target_ip": "2001:db8:10::20",
        "destination_multicast": False, "solicited_flag": True
    }
    cases = [
        ("normal NS", ns, True),
        ("DAD NS", {**ns, "source_ip": "::",
                     "has_source_lladdr": False}, True),
        ("invalid DAD option", {**ns, "source_ip": "::"}, False),
        ("valid NA", na, True),
        ("multicast NA solicited", {**na, "destination_multicast": True}, False),
        ("wrong hop limit", {**ns, "hop_limit": 64}, False),
        ("multicast target", {**ns, "target_ip": "ff02::1"}, False),
    ]
    for label, record, expected in cases:
        valid, reason = review(record)
        assert valid is expected, (label, reason)
        print(f"{label:24} {'CONSISTENT' if valid else 'REVIEW':10} | {reason}")
    print("Offline checks passed; no network packets were sent.")


if __name__ == "__main__":
    main()
