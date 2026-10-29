"""Find overlapping CIDR blocks in a synthetic IP address plan."""
from ipaddress import ip_network
from itertools import combinations

PLAN = {
    "office": "10.10.0.0/16",
    "datacenter": "10.20.0.0/16",
    "vpn": "10.10.64.0/20",     # inside office
    "guest": "192.168.50.0/24",
}

def overlaps(plan):
    nets = {name: ip_network(cidr) for name, cidr in plan.items()}
    return [(a, b) for a, b in combinations(nets, 2) if nets[a].overlaps(nets[b])]

if __name__ == "__main__":
    for a, b in overlaps(PLAN):
        print(f"overlap: {a} ({PLAN[a]}) and {b} ({PLAN[b]})")
    assert overlaps(PLAN) == [("office", "vpn")]
    print("Note: intentional sub-allocation is fine when documented; accidental overlap breaks routing and firewall rules.")
