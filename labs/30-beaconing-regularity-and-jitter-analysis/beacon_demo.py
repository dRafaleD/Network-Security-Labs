"""Score the regularity of connection intervals using the coefficient of variation."""
import statistics

SERIES = {
    "agent-like": [0, 60, 120, 181, 240, 300, 361, 420, 480, 541],
    "human-browsing": [0, 5, 70, 74, 300, 305, 309, 700, 910, 913],
    "jittered": [0, 55, 130, 170, 255, 300, 380, 415, 505, 540],
}


def variation(times):
    gaps = [b - a for a, b in zip(times, times[1:])]
    return statistics.pstdev(gaps) / statistics.mean(gaps)


def is_regular(times, threshold=0.1, min_events=8):
    return len(times) >= min_events and variation(times) < threshold


if __name__ == "__main__":
    for name, t in SERIES.items():
        print(f"{name:15} variation={variation(t):.2f} regular={is_regular(t)}")
    assert is_regular(SERIES["agent-like"])
    assert not is_regular(SERIES["human-browsing"])
    assert not is_regular(SERIES["jittered"])
    assert not is_regular(SERIES["agent-like"][:4])
    print("PASS: near-fixed intervals are flagged; jitter and short series are not.")
    print("Review: updaters are regular too, and jitter defeats this check on its own.")
