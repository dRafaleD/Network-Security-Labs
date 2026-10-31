"""Audit synthetic SNMP configurations for defaults, write access and open source ranges."""
DEVICES = [
    {"name": "sw1", "version": "v2c", "community": "public", "access": "ro", "allowed": "0.0.0.0/0"},
    {"name": "rtr1", "version": "v2c", "community": "k7Q-long-random-9xZ", "access": "rw", "allowed": "10.0.9.0/24"},
    {"name": "fw1", "version": "v3", "community": None, "access": "ro", "allowed": "10.0.9.0/24"},
]
DEFAULTS = {"public", "private", "community"}


def findings(d):
    out = []
    if d["version"] in ("v1", "v2c"):
        out.append("uses community strings sent in clear text")
        if d["community"] in DEFAULTS:
            out.append("default community string")
    if d["access"] == "rw":
        out.append("write access enabled")
    if d["allowed"] == "0.0.0.0/0":
        out.append("reachable from any address")
    return out


if __name__ == "__main__":
    for d in DEVICES:
        print(f"{d['name']:5} {findings(d)}")
    assert len(findings(DEVICES[0])) == 3
    assert len(findings(DEVICES[1])) == 2
    assert findings(DEVICES[2]) == []
    print("PASS: defaults, write access and wide ranges are reported; v3 with limits is clean.")
    print("Review: configuration audits do not prove reachability; test both.")
