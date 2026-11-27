"""Aggregate invented nonoverlapping flow intervals; no network I/O."""
from fractions import Fraction

def summarize(rows):
    total=duration=0
    last=None
    for start,end,delta in sorted(rows):
        if any(type(x) is not int for x in (start,end,delta)) or end<=start or delta<0:
            return "INVALID",None
        if last is not None and start<last:
            return "OVERLAP",None
        last=end
        total+=delta
        duration+=end-start
    if not duration:
        return "NO_COVERAGE",None
    span=max(r[1] for r in rows)-min(r[0] for r in rows)
    return "OK",{"rate":Fraction(total,duration),
                 "coverage":Fraction(duration,span)}

def main():
    cases=[
        ([(0,2,100),(2,10,100)],("OK",{"rate":Fraction(20),"coverage":Fraction(1)})),
        ([(0,2,100),(8,10,100)],("OK",{"rate":Fraction(50),"coverage":Fraction(2,5)})),
        ([(2,4,0)],("OK",{"rate":Fraction(0),"coverage":Fraction(1)})),
        ([(2,4,1)],("OK",{"rate":Fraction(1,2),"coverage":Fraction(1)})),
        ([(0,3,1),(2,4,1)],("OVERLAP",None)),
        ([(0,0,1)],("INVALID",None)),
        ([(0,1,-1)],("INVALID",None)),
        ([],("NO_COVERAGE",None)),
    ]
    for rows,want in cases:
        got=summarize(rows)
        assert got==want,(got,want)
        print(got)
    print("8/8 aggregate cases passed")

if __name__=="__main__":
    main()
