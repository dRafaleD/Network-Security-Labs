"""Flag destinations with many SYNs but few completed handshakes (synthetic counters)."""
COUNTERS = {
    "10.0.1.10:443": {"syn": 1000, "established": 950},
    "10.0.1.20:80": {"syn": 50000, "established": 400},
    "10.0.1.30:22": {"syn": 30, "established": 5},
}


def suspects(counters, min_syn=1000, max_ratio=0.1):
    out = []
    for dst, c in counters.items():
        ratio = c["established"] / c["syn"]
        if c["syn"] >= min_syn and ratio <= max_ratio:
            out.append((dst, round(ratio, 3)))
    return out


if __name__ == "__main__":
    out = suspects(COUNTERS)
    print(out)
    assert [d for d, _ in out] == ["10.0.1.20:80"]
    print("PASS: high SYN volume with very low completion is flagged; a low volume is not.")
    print("Review: server overload looks similar, and spoofed sources make attribution unreliable.")
