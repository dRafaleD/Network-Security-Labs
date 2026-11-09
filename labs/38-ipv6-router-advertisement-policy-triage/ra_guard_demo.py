#!/usr/bin/env python3
"""Synthetic IPv6 Router Advertisement policy review; zero network I/O."""
from ipaddress import IPv6Address, IPv6Network

EXPECTED_SEGMENT = "lab-segment-a"
EXPECTED_PREFIX = IPv6Network("2001:db8:10::/64")
APPROVED_ROUTERS = {
    ("fe80::1", "02:00:5e:00:53:01")
}


def check_ra(record: dict) -> tuple[bool, str]:
    if record.get("segment") != EXPECTED_SEGMENT:
        return False, "segment not recognized"
    if record.get("icmpv6_type") != 134:
        return False, "not an RA record"
    if record.get("hop_limit") != 255:
        return False, "invalid NDP Hop Limit"

    try:
        address = IPv6Address(record["source_ip"])
        prefix = IPv6Network(record["prefix"], strict=True)
    except (ValueError, KeyError, TypeError) as error:
        return False, f"invalid address/prefix: {error}"

    if not address.is_link_local:
        return False, "RA source is not link-local"
    # This is an operational policy check, NOT cryptographic authentication.
    identity = (str(address), str(record.get("source_mac", "")).lower())
    if identity not in APPROVED_ROUTERS:
        return False, "unrecognized router identity"
    if prefix != EXPECTED_PREFIX:
        return False, "unexpected advertised prefix"
    return True, "consistent with configured training policy"


def main():
    baseline = {
        "segment": EXPECTED_SEGMENT, "icmpv6_type": 134,
        "hop_limit": 255, "source_ip": "fe80::1",
        "source_mac": "02:00:5e:00:53:01",
        "prefix": "2001:db8:10::/64"
    }
    events = [
        ("approved baseline", baseline, True),
        ("unknown router", {**baseline, "source_ip": "fe80::99"}, False),
        ("unexpected prefix", {**baseline, "prefix": "2001:db8:11::/64"}, False),
        ("invalid hop limit", {**baseline, "hop_limit": 64}, False),
        ("off-link source", {**baseline, "source_ip": "2001:db8::1"}, False),
    ]
    for label, record, expected in events:
        accepted, reason = check_ra(record)
        assert accepted is expected, (label, reason)
        print(f"{label:20} {'ALLOW' if accepted else 'REVIEW':6} | {reason}")
    print("Checks passed. Address/MAC agreement cannot rule out spoofing.")


if __name__ == "__main__":
    main()
