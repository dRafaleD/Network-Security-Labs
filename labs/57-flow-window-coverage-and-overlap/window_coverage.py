"""Offline review of invented measurement intervals."""
from fractions import Fraction

def coverage(windows, start, end):
    if end <= start:
        return "INVALID_WINDOW", None
    if any(b <= a or a < start or b > end for a,b in windows):
        return "INVALID_INTERVAL", None
    merged = []
    overlap = False
    for a,b in sorted(windows):
        if merged and a <= merged[-1][1]:
            overlap |= a < merged[-1][1]
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a,b))
    covered = sum(b-a for a,b in merged)
    return ("OVERLAP_REVIEW" if overlap else "COVERAGE"), Fraction(covered,end-start)

def main():
    cases = [
        ([],0,10,("COVERAGE",Fraction(0))),
        ([(0,10)],0,10,("COVERAGE",Fraction(1))),
        ([(0,4),(6,10)],0,10,("COVERAGE",Fraction(4,5))),
        ([(0,5),(5,10)],0,10,("COVERAGE",Fraction(1))),
        ([(0,6),(4,10)],0,10,("OVERLAP_REVIEW",Fraction(1))),
        ([(0,8),(2,3)],0,10,("OVERLAP_REVIEW",Fraction(4,5))),
        ([(0,5),(0,5)],0,10,("OVERLAP_REVIEW",Fraction(1,2))),
        ([(0,11)],0,10,("INVALID_INTERVAL",None)),
        ([(3,3)],0,10,("INVALID_INTERVAL",None)),
        ([],10,0,("INVALID_WINDOW",None)),
    ]
    for rows,start,end,expected in cases:
        result=coverage(rows,start,end)
        assert result==expected,(rows,result)
        print(result)
    print("10/10 coverage cases passed")

if __name__ == "__main__":
    main()
