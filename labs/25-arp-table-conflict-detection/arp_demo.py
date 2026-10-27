"""Spot IP/MAC conflicts in a synthetic ARP observation log."""
from collections import defaultdict

OBSERVATIONS = [
    ("192.0.2.1", "aa:aa:aa:00:00:01", 0),
    ("192.0.2.20", "aa:aa:aa:00:00:20", 1),
    ("192.0.2.1", "aa:aa:aa:00:00:01", 60),
    ("192.0.2.1", "bb:bb:bb:00:00:99", 61),   # same IP, new MAC
    ("192.0.2.30", "aa:aa:aa:00:00:20", 70),  # same MAC, second IP
]

def conflicts(observations):
    ip_to_macs, mac_to_ips = defaultdict(set), defaultdict(set)
    for ip, mac, _ in observations:
        ip_to_macs[ip].add(mac)
        mac_to_ips[mac].add(ip)
    return ({ip: sorted(m) for ip, m in ip_to_macs.items() if len(m) > 1},
            {mac: sorted(i) for mac, i in mac_to_ips.items() if len(i) > 1})

if __name__ == "__main__":
    ip_conflicts, mac_conflicts = conflicts(OBSERVATIONS)
    print("IP with several MACs:", ip_conflicts)
    print("MAC with several IPs:", mac_conflicts)
    assert "192.0.2.1" in ip_conflicts
    print("Note: failover, VRRP, NIC replacement and multi-homed hosts cause the same pattern; confirm with the switch port table.")
