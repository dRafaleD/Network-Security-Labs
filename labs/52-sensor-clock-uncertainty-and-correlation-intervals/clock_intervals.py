"""Offline correlation of fictional sensor time intervals."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Observation:
    origin: str
    event: str
    earliest: int
    latest: int

def correlate(rows):
    if not rows:
        return "NO_EVIDENCE"
    by_origin = {}
    for row in rows:
        if row.earliest > row.latest:
            return "INVALID_INTERVAL"
        previous = by_origin.get(row.origin)
        if previous is not None and previous != row:
            return "ORIGIN_CONFLICT"
        by_origin[row.origin] = row
    values = list(by_origin.values())
    if len({r.event for r in values}) != 1:
        return "EVENT_CONFLICT"
    if len(values) == 1:
        return "SINGLE_ORIGIN"
    if max(r.earliest for r in values) > min(r.latest for r in values):
        return "DISJOINT_INTERVALS"
    return "POSSIBLE_TIME_MATCH"

def main():
    a = Observation("a", "DAD_FAIL", 98, 102)
    b = Observation("b", "DAD_FAIL", 101, 104)
    cases = [
        ([], "NO_EVIDENCE"),
        ([a], "SINGLE_ORIGIN"),
        ([a,a], "SINGLE_ORIGIN"),
        ([a,b], "POSSIBLE_TIME_MATCH"),
        ([a,Observation("b","DAD_FAIL",103,106)], "DISJOINT_INTERVALS"),
        ([a,Observation("b","DAD_OK",99,101)], "EVENT_CONFLICT"),
        ([a,Observation("a","DAD_FAIL",99,103)], "ORIGIN_CONFLICT"),
        ([Observation("a","DAD_FAIL",105,100)], "INVALID_INTERVAL"),
        ([a,Observation("b","DAD_FAIL",102,105)], "POSSIBLE_TIME_MATCH"),
    ]
    for rows, expected in cases:
        actual = correlate(rows)
        assert actual == expected, (actual, expected)
        print(actual)
    print(f"{len(cases)}/{len(cases)} synthetic interval checks passed")

if __name__ == "__main__":
    main()
