"""Detect ICMP ping sweeps: many distinct destinations from one source inside a time window."""
from collections import defaultdict

EVENTS = (
    [("10.0.0.5", f"10.0.1.{i}", i) for i in range(1, 31)]       # 30 hosts in 30 s
    + [("10.0.0.7", "10.0.1.10", t) for t in range(0, 60, 2)]    # one host, repeated
    + [("10.0.0.9", f"10.0.2.{i}", i * 40) for i in range(1, 12)]  # 11 hosts over 440 s: too slow
)


def sweeps(events, window=60, min_hosts=20):
    by_src = defaultdict(list)
    for src, dst, t in events:
        by_src[src].append((t, dst))
    flagged = []
    for src, items in by_src.items():
        items.sort()
        for i, (t0, _) in enumerate(items):
            hosts = {d for t, d in items[i:] if t - t0 <= window}
            if len(hosts) >= min_hosts:
                flagged.append(src)
                break
    return sorted(flagged)


if __name__ == "__main__":
    out = sweeps(EVENTS)
    print("flagged:", out)
    assert out == ["10.0.0.5"]
    print("PASS: many hosts in a short window are flagged; repeats and slow scans are not.")
    print("Review: slow sweeps evade a short window, and monitoring hosts look the same.")
