"""Fictional offline counter samples; no network I/O."""
from fractions import Fraction

def rate(previous,current):
    # Each sample is (time, cumulative bytes, boot identity).
    t0,b0,boot0=previous
    t1,b1,boot1=current
    if any(type(x) is not int for x in (t0,t1,b0,b1)) or min(b0,b1)<0:
        return "INVALID",None
    if t1<=t0:
        return "INVALID_TIME",None
    if boot0!=boot1:
        return "RESET_UNKNOWN",None
    if b1<b0:
        return "COUNTER_REGRESSION",None
    if t1-t0>10:
        return "COVERAGE_GAP",None
    return "RATE",Fraction(b1-b0,t1-t0)

def main():
    old=(100,200,"a")
    cases=[
        ((102,300,"a"),("RATE",Fraction(50))),
        ((105,300,"a"),("RATE",Fraction(20))),
        ((103,201,"a"),("RATE",Fraction(1,3))),
        ((110,200,"a"),("RATE",Fraction(0))),
        ((111,500,"a"),("COVERAGE_GAP",None)),
        ((102,100,"a"),("COUNTER_REGRESSION",None)),
        ((102,10,"b"),("RESET_UNKNOWN",None)),
        ((100,250,"a"),("INVALID_TIME",None)),
        ((99,250,"a"),("INVALID_TIME",None)),
        ((102,-1,"a"),("INVALID",None)),
        ((102,True,"a"),("INVALID",None)),
    ]
    for sample,want in cases:
        got=rate(old,sample)
        assert got==want,(sample,got,want)
        print(sample,got)
    print("11/11 flow-rate cases passed")

if __name__=="__main__":
    main()
