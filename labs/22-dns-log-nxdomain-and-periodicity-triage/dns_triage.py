"""Summarize synthetic DNS log lines: NXDOMAIN ratio and query regularity per client."""
from collections import defaultdict
from statistics import pstdev

# (client, seconds since start, response code)
LOG = [
    ("10.0.0.5", 0, "NOERROR"), ("10.0.0.5", 60, "NXDOMAIN"), ("10.0.0.5", 120, "NXDOMAIN"),
    ("10.0.0.5", 180, "NXDOMAIN"), ("10.0.0.5", 240, "NXDOMAIN"),
    ("10.0.0.9", 0, "NOERROR"), ("10.0.0.9", 17, "NOERROR"), ("10.0.0.9", 95, "NOERROR"),
    ("10.0.0.9", 101, "NXDOMAIN"), ("10.0.0.9", 230, "NOERROR"),
]

def summarize(log):
    by_client = defaultdict(list)
    for client, ts, rcode in log:
        by_client[client].append((ts, rcode))
    report = {}
    for client, rows in by_client.items():
        times = [t for t, _ in rows]
        gaps = [b - a for a, b in zip(times, times[1:])]
        nx = sum(1 for _, r in rows if r == "NXDOMAIN") / len(rows)
        report[client] = {"nxdomain_ratio": round(nx, 2), "gap_stdev": round(pstdev(gaps), 1)}
    return report

if __name__ == "__main__":
    for client, stats in summarize(LOG).items():
        print(client, stats)
    print("Note: regular timing and high NXDOMAIN ratios are triage leads only; software updaters and misconfigurations look similar.")
