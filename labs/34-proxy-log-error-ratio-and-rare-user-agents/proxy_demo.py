"""Triage a synthetic proxy log: per-client error ratio and rare user agents."""
from collections import Counter, defaultdict

LOG = [
    ("10.0.0.5", 200, "Mozilla/5.0"), ("10.0.0.5", 200, "Mozilla/5.0"), ("10.0.0.5", 404, "Mozilla/5.0"),
    ("10.0.0.6", 403, "tool-x/1.0"), ("10.0.0.6", 403, "tool-x/1.0"), ("10.0.0.6", 404, "tool-x/1.0"),
    ("10.0.0.7", 200, "Mozilla/5.0"), ("10.0.0.7", 200, "Mozilla/5.0"), ("10.0.0.7", 200, "Mozilla/5.0"),
]

def summarize(log):
    per_client = defaultdict(list)
    agents = Counter(agent for _, _, agent in log)
    for client, status, agent in log:
        per_client[client].append(status)
    rows = {}
    for client, statuses in per_client.items():
        errors = sum(1 for s in statuses if s >= 400)
        rows[client] = round(errors / len(statuses), 2)
    rare = [agent for agent, count in agents.items() if count <= 3]
    return rows, rare

if __name__ == "__main__":
    ratios, rare = summarize(LOG)
    print("error ratio per client:", ratios)
    print("rare user agents:", rare)
    assert ratios["10.0.0.6"] == 1.0
    print("Note: scanners, broken scripts and legitimate tools share this pattern; correlate with the destination and the user.")
