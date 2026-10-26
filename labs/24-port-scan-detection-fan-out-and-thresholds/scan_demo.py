"""Flag a possible port scan from synthetic connection records using fan-out per source."""
from collections import defaultdict

EVENTS = (
    [("10.0.0.5", "10.0.1.20", p) for p in range(1, 41)]          # one host, many ports
    + [("10.0.0.7", "10.0.1.20", 443)] * 30                         # repeated, one port
    + [("10.0.0.9", f"10.0.1.{i}", 443) for i in range(1, 31)]      # many hosts, one port
)


def fan_out(events):
    ports, hosts = defaultdict(set), defaultdict(set)
    for src, dst, port in events:
        ports[(src, dst)].add(port)
        hosts[(src, port)].add(dst)
    return ports, hosts


def alerts(events, port_threshold=20, host_threshold=20):
    ports, hosts = fan_out(events)
    out = [("port-scan", s, d) for (s, d), p in ports.items() if len(p) >= port_threshold]
    out += [("sweep", s, p) for (s, p), h in hosts.items() if len(h) >= host_threshold]
    return sorted(out)


if __name__ == "__main__":
    for a in alerts(EVENTS):
        print(a)
    kinds = {a[1]: a[0] for a in alerts(EVENTS)}
    assert kinds["10.0.0.5"] == "port-scan"
    assert kinds["10.0.0.9"] == "sweep"
    assert "10.0.0.7" not in kinds
    print("PASS: fan-out flags many-port and many-host patterns, not repeated traffic.")
    print("Review: a vulnerability scanner or monitoring host will look the same.")
