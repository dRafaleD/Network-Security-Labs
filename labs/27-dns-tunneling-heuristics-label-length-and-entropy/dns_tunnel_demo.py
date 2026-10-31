"""Score synthetic DNS query names for tunneling using label length and Shannon entropy."""
import math
from collections import Counter, defaultdict

QUERIES = (
    ["www.example.test", "mail.example.test", "api.example.test"] * 5
    + [f"{label}.t.badzone.test" for label in (
        "mfrggzdfmztwq2lknnwg23tpobyxe43uov3ho6dzpiaqaaaaaaa",
        "gezdgnbvgy3tqojqmfrggzdfmztwq2lknnwg23tpobyxe43uov3",
        "nb2hi4dthixs653xo4xgs3tfm5uhg3dpnzqxg2dbnqxgy5dfmqq",
        "mnxw2zlbmjuwy2lunbsxg5dtnfzxi33jmzzgk5tfnvsxeylsnru",
    )]
)


def entropy(text):
    counts = Counter(text)
    return -sum((n / len(text)) * math.log2(n / len(text)) for n in counts.values())


def suspects(queries, min_len=30, min_entropy=3.5, min_names=3):
    by_domain = defaultdict(set)
    for q in queries:
        label, _, rest = q.partition(".")
        if len(label) >= min_len and entropy(label) >= min_entropy:
            by_domain[rest].add(q)
    return sorted(d for d, names in by_domain.items() if len(names) >= min_names)


if __name__ == "__main__":
    print("entropy(www)  :", round(entropy("www") + 0.0, 2))
    print("entropy(label):", round(entropy(QUERIES[-1].split(".")[0]), 2))
    result = suspects(QUERIES)
    print("suspected tunnels:", result)
    assert result == ["t.badzone.test"]
    assert "example.test" not in result
    print("PASS: many long, high-entropy labels under one domain are flagged.")
    print("Review: CDNs also use random labels, and encrypted DNS hides names from this check.")
