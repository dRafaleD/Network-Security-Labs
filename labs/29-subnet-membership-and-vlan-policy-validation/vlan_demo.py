"""Validate that host addresses fall inside the subnet assigned to their VLAN."""
import ipaddress

VLANS = {10: "10.0.1.0/24", 20: "10.0.10.0/24"}
HOSTS = [
    ("web1", 10, "10.0.1.5"),
    ("db1", 20, "10.0.10.5"),
    ("printer", 10, "10.0.10.77"),    # wrong VLAN's subnet
    ("laptop", 20, "10.0.100.9"),     # shares the string prefix "10.0.10" but is outside
]


def violations(hosts):
    out = []
    for name, vlan, ip in hosts:
        if ipaddress.ip_address(ip) not in ipaddress.ip_network(VLANS[vlan]):
            out.append(f"{name}: {ip} is outside {VLANS[vlan]} (VLAN {vlan})")
    return out


if __name__ == "__main__":
    out = violations(HOSTS)
    for line in out:
        print(line)
    assert len(out) == 2
    assert all("web1" not in o and "db1" not in o for o in out)
    print("PASS: membership is checked with real network math, not string prefixes.")
    print("Review: the mapping goes stale, and this says nothing about inter-VLAN firewall rules.")
