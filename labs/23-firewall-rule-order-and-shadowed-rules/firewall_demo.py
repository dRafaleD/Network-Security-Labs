"""First-match firewall model that reports shadowed rules (synthetic rules only)."""
from ipaddress import ip_address, ip_network

RULES = [
    ("allow", "10.0.0.0/8", 443),
    ("deny", "10.1.0.0/16", 443),   # shadowed: the broader allow above matches first
    ("deny", "0.0.0.0/0", 23),
    ("allow", "0.0.0.0/0", 80),
]

def decide(src, port, rules=RULES):
    for index, (action, net, rule_port) in enumerate(rules):
        if ip_address(src) in ip_network(net) and port == rule_port:
            return action, index
    return "deny", None  # default deny

def shadowed(rules=RULES):
    found = []
    for j, (_, net_j, port_j) in enumerate(rules):
        for i in range(j):
            _, net_i, port_i = rules[i]
            if port_i == port_j and ip_network(net_j).subnet_of(ip_network(net_i)):
                found.append((j, i))
    return found

if __name__ == "__main__":
    print(decide("10.1.2.3", 443))
    print(decide("192.0.2.9", 25))
    print("shadowed (rule, shadowed_by):", shadowed())
    assert decide("10.1.2.3", 443) == ("allow", 0)
    print("Note: real firewalls add states, zones and negation; verify with a rule-hit test on the actual device.")
